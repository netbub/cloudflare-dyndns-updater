# cloudflare-dyndns-updater

This script takes in a domain fronted by Cloudflare and checks
if the current IP matches the IP for that domain's DNS record. If it doesn't,
the DNS record is updated.

## Authenticate to Cloudflare

Either set CLOUDFLARE_API_KEY as an environment varaiable with the value of your API key,
or create a file called ".env" with the following syntax:

```txt
CLOUDFLARE_API_KEY=value
```
