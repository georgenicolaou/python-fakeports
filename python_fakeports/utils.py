import sqlite3, os
if os.name != 'nt':
    import iptc
else:
    print("[Warning] Windows does not support iptables")

def forward_local_port(iface, dport, to_port, proto="tcp"):
    if isinstance(dport, list):
        multiport = True
    else:
        multiport = False

    table = iptc.Table(iptc.Table.NAT)
    chain = iptc.Chain(table, "PREROUTING")

    rule = iptc.Rule()
    rule.in_interface = str(iface)
    rule.protocol = proto

    match = iptc.Match(rule, proto if multiport is False else "multiport")
    if multiport:
        match.dports = ",".join([str(p) for p in dport])
    else:
        match.dport = str(dport)
    rule.add_match(match)

    target = iptc.Target(rule, "REDIRECT")
    target.to_ports = str(to_port)
    rule.target = target

    chain.insert_rule(rule)

    return True

def delete_forward_local_port(iface, dport, to_port, proto="tcp"):
    if isinstance(dport, list):
        multiport = True
    else:
        multiport = False

    deleted = False
    chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "PREROUTING")
    for rule in chain.rules:
        if rule.in_interface == str(iface) and rule.protocol == proto:
            if rule.target.to_ports == to_port:
                if multiport:
                    if set(dport) == set(rule.matches[0].dports.split(",")):
                        chain.delete_rule(rule)
                        deleted = True
                else:
                    if str(dport) == rule.matches[0].dport:
                        chain.delete_rule(rule)
                        deleted = True
    return deleted

class SignaturesStore():
    def __init__(self, dbpath, new=False):
        if os.path.isfile(dbpath) is False:
            new = True
        elif new:
            os.remove(dbpath)
        self.conn = sqlite3.connect(dbpath)
        if new:
            self.install()

    def install(self):
        cur = self.conn.cursor()
        cur.execute(
            """CREATE TABLE nmap_signatures (
                  id INTEGER PRIMARY KEY,
                  signature VARCHAR,
                  prog_name VARCHAR,
                  version_arg_location INTEGER
              )"""
        )
        self.conn.commit()
        cur.close()

    def add_signature(self, signature, prog_name, version_arg_location):
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO nmap_signatures (signature, prog_name, version_arg_location) VALUES (?, ?, ?)""",
            (signature, prog_name, version_arg_location)
        )
        self.conn.commit()
        cur.close()

    def search(self, prog_name):
        cur = self.conn.cursor()
        tokens = [ '%'+tok+'%' for tok in prog_name.split(" ") ]
        prog_name_where = "prog_name LIKE ?" + " AND prog_name LIKE ?" *  ( len(tokens) - 1 )
        sql = "SELECT * FROM nmap_signatures WHERE " + prog_name_where
        cur.execute(sql, tokens)
        return cur.fetchall()

    def get(self, id):
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM nmap_signatures WHERE id = ?""", (id,))
        return cur.fetchall()

    def close(self):
        self.conn.close()