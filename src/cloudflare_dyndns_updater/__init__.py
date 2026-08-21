import os
import sys

import requests
from cloudflare import Cloudflare


def main() -> None:
    client = Cloudflare(api_token=os.environ.get("CLOUDFLARE_API_TOKEN"))
    zone_id = client.zones.list(name="netbub.com").result[0].id
    records = client.dns.records.list(zone_id=zone_id).result
    record_id = ""
    last_ip = ""
    for record in records:
        if record.name == "pz.netbub.com":
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
            name="pz.netbub.com",
            ttl=3600,
            type="A",
            content=current_ip,
        )
        if not record_response:
            print(record_response)
            raise Exception(record_response)
    else:
        print("IP has not changed, not updating Cloudflare record")


if __name__ == "__main__":
    sys.exit(main())
