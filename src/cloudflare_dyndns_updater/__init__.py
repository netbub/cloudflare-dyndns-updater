import argparse
import os
import sys
from pathlib import Path

import requests
from cloudflare import Cloudflare


def updater(args: argparse.Namespace) -> None:
    envVars = {}
    if Path(".env").exists():
        with open(".env") as fp:
            for line in fp:
                k = line.split("=")[0]
                v = line.split("=")[1]
                envVars[k] = v.strip('"')
        client = Cloudflare(api_token=envVars["CLOUDFLARE_API_TOKEN"])  # type: ignore
    else:
        client = Cloudflare(api_token=os.environ.get("CLOUDFLARE_API_TOKEN"))
    zone = ".".join(args.domain.split(".")[1:])
    print(client)
    zone_id = client.zones.list(name=zone).result[0].id
    records = client.dns.records.list(zone_id=zone_id).result
    record_id = ""
    last_ip = ""
    for record in records:
        if record.name == args.domain:
            record_id = record.id
    record = client.dns.records.get(dns_record_id=record_id, zone_id=zone_id)
    last_ip = record.content
    current_ip_req = requests.get("https://v4.ipify.io")
    current_ip = current_ip_req.text
    try:
        current_ip_req.raise_for_status()
    except Exception as e:
        print(type(e))
        print(e.args)
        print(e)
        raise

    if current_ip != last_ip:
        record_response = client.dns.records.update(
            dns_record_id=record_id,
            zone_id=zone_id,
            name=args.domain,
            ttl=3600,
            type="A",
            content=current_ip,
        )
        if not record_response:
            print(record_response)
            raise Exception(record_response)
    else:
        print("IP has not changed, not updating Cloudflare record")


def main():
    parser = argparse.ArgumentParser(
        prog="cloudflare_dyndns_updater",
        description="Checks the IP of the host and, if the domain provided is different, changes the given Cloudflare record",
    )
    parser.add_argument("domain", help="domain name")
    args = parser.parse_args()
    sys.exit(updater(args))
