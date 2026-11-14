import re
import ipaddress
from datetime import datetime


logRegex = re.compile(r'(?P<time>^\w{3}\s+\d{1,2}\s\d\d:\d\d:\d\d)\s\w+\s\S+\s(?P<success>Failed|Accepted)\s\w+\sfor\s(?:invalid user\s)?(?P<user>\S+)\s\w+\s(?P<ip>[0-9a-fA-F:.]+).+')

def parse_ssh_line(line):
    match = logRegex.search(line)

    if match is not None:
        try:
            ip = str(ipaddress.ip_address(match.group("ip")))
        except ValueError:
            return None

        time = datetime.strptime(f"{datetime.now().year}", "%Y %b %d %H:%M:%S")
        
        event_dict = match.groupdict()
        event_dict["ip"] = ip

        return event_dict
    else:
        return None





with open("auth.log", encoding="utf-8", errors="replace") as f:
    for line in f:
        print(parse_ssh_line(line.rstrip()))