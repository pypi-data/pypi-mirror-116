"""
### ufw default policies
# sudo ufw default deny incoming
# sudo ufw default allow outgoing

# sudo ufw allow ssh
# sudo ufw allow http
# sudo ufw allow https
# sudo ufw allow ssl

# sudo ufw allow from 10.0.0.1

## deny all ssh, but allow from ip
# sudo ufw allow from 10.0.0.1 to any port 22
# sudo ufw allow from <ip> to any port 80

## deny
# ufw status numbered
# sudo ufw delete [:rule-number]

# sudo ufw deny icmp
# sudo ufw deny from <ip>
"""
import gettext
import re
from typing import List, Any, AnyStr

from ufw.backend_iptables import UFWBackendIptables
from ufw.common import programName
from ufw.frontend import UFWFrontend, parse_command

gettext.install(programName)


class EzUFW(UFWFrontend):
    """
    Class which extends UFWFrontend and allows manipulate UFW.
    """

    """Splitter for commands. Includes more than 1 space."""
    SPLITTER = re.compile(r'\s+')

    """Ports splitter. Default is ','"""
    PORT_SPLITTER = re.compile(r',')

    """IPv4 regex"""

    IPV4_REGEX = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    EMPTY = ""

    def __init__(self, dry_run: bool = False, backend_type: str = "iptables", root_dir: str = None, data_dir: str = None):
        super().__init__(dryrun=dry_run, backend_type=backend_type, rootdir=root_dir, datadir=data_dir)
        self.dry_run = dry_run
        self.root_dir = root_dir
        self.data_dir = data_dir

    def refresh_backend(self) -> UFWBackendIptables:
        """
        Refresh is necessary if changes have been performed with UFWFrontend.

        :return: UFWBackendIptables, refreshed backend.
        """
        self.backend = UFWBackendIptables(self.dry_run, rootdir=self.root_dir, datadir=self.data_dir)
        return self.backend

    def rules(self) -> List:
        """
        :return: list of stored rules from UFW.
        """
        return self.refresh_backend().get_rules()

    def _command(self, *cmd: Any) -> AnyStr:
        """
        Inner method to build command using UFW command parser.

        :param cmd: arguments for command.
        :return: string, parsed command.
        """
        command = [programName]
        for c in cmd:
            command.extend(self.SPLITTER.split(str(c)))

        return parse_command(command)

    def execute(self, *cmd, force: bool = False) -> None:
        """
        Execute provided command with UFW.

        :param cmd: arguments for command.
        :param force: True if force, otherwise False. False by default.
        :return:
        """
        ufw_cmd = self._command(*cmd)
        rule = ufw_cmd.data.get('rule', self.EMPTY)
        ip_type = ufw_cmd.data.get('iptype', self.EMPTY)
        return self.do_action(ufw_cmd.action, rule, ip_type, force)

    def reset(self, default_policies: bool = True, force: bool = True) -> None:
        """
        Reset UFW configuration.
        Default policies includes:
        * default deny incoming,
        * default allow outgoing.

        :param default_policies: default True. Default policies will be applied.
        :param force: True if force, otherwise False. True by default.
        :return:
        """
        self.execute('reset', force=force)
        if default_policies:
            self.execute("default", "deny", "incoming", force=force)
            self.execute("default", "allow", "outgoing", force=force)

    def enable(self) -> None:
        """
        Enable the UFW.
        """
        self.set_enabled(True)

    def disable(self) -> None:
        """
        Disable the UFW.
        """
        self.set_enabled(False)

    def delete_by_port(self, *ports : Any) -> List:
        """
        Remove the rules connected with specified port. Counter keep numbering for the rule.
        When the rule is removed from ufw other rules are lifted and rules' indexes are changed.

        @return list of removed rules.
        """
        removed_rules = []
        selected_ports = [max(0, int(port)) for port in ports]

        counter = 1
        for rule in self.rules():
            rule_port = -1 if rule.dport is None else int(rule.dport)
            if rule_port in selected_ports:
                removed_rules.append(rule)
                self.execute("delete", counter, force=True)
            else:
                counter += 1

        return removed_rules

    def delete_by_ip(self, *ip_address: Any) -> List:
        """
        Remove the rules connected to specific ip_address.
        """
        removed_rules = []
        counter = 1
        for rule in self.rules():
            if rule.src in ip_address:
                removed_rules.append(rule)
                self.execute("delete", counter, force=True)
            else:
                counter += 1

        return removed_rules

    def deny(self, port: int = None, protocol: int = None):
        values = []
        if port is not None:
            values.append(port)
            if protocol is not None:
                values.append("/")
                values.append(protocol)
        return self.denyA(None if not values else "".join(map(str, values)))

    def denyA(self, port_and_protocol=None):
        cmd = ('default', 'deny') if port_and_protocol is None else ("deny", port_and_protocol)
        return self.execute(*cmd)

    def deny_from(self, ip_address: str, *ports: Any):
        if ports:
            for port in ports:
                self.execute("deny", "from", ip_address, "to", "any", "port", port)
        else:
            self.execute("deny", "from", ip_address)

    def allow_from(self, ip_address: str, *ports: Any):
        if ports:
            for port in ports:
                self.execute("allow", "from", ip_address, "to", "any", "port", port)
        else:
            self.execute("allow", "from", ip_address)

    def insert(self, ip_address: str, index: int = 1, comment: str = ""):
        """
        UFW (iptables) rules are applied in order of insertion. When the rule is matched other rules are skipped.
        In case when given IP should be banned, the rule must be on top.
        """
        cmd = ["insert", index, "deny", "from", ip_address]
        if comment:
            cmd.extend(["comment", comment])
        return self.execute(*cmd)

    def status(self, verbose: bool = True):
        cmd = ("status", "verbose") if verbose else ("status",)
        return self.execute(*cmd)

