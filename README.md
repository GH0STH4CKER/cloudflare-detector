# Cloudflare Detection Tool

A simple Python script that checks whether a domain or URL is likely using Cloudflare by analyzing:

- DNS A/AAAA/CNAME records
- Known Cloudflare IP ranges
- Cloudflare-specific HTTP response headers
- Server and cookies
- Socket resolution

## Requirements

Install the required Python packages:

```bash
pip install requests dnspython
```

## Usage

Run the script with a domain or URL:

```bash
python cloudflareCheck.py example.com
```

or

```bash
python cloudflareCheck.py https://example.com
```

## Example Input

```bash
python cloudflareCheck.py https://www.cloudflare.com
```

## Example Output (Cloudflare Detected)

```
╔════════════════════════════════════════════════════════╗
║         Cloudflare Detection Tool                      ║
╚════════════════════════════════════════════════════════╝

Target: https://www.cloudflare.com
Domain: www.cloudflare.com

[1] DNS Analysis
------------------------------------------------------------
A     : 104.16.123.96, 104.16.123.97
AAAA  : 2606:4700::6810:7b60, 2606:4700::6810:7b61
CNAME : Not found

[+] Cloudflare IP detected

[2] HTTP Analysis
------------------------------------------------------------
Final URL : https://www.cloudflare.com/
Status    : 200
Server    : cloudflare

Cloudflare Headers:
  [+] CF-Ray: 8c5f1a2b3c4d5e6f
  [+] CF-Cache-Status: HIT

[+] Server header indicates Cloudflare

Cloudflare Cookies:
  [-] No obvious Cloudflare cookies found.

[3] Socket Resolution
------------------------------------------------------------
Resolved IP: 104.16.123.96
[+] IP belongs to a Cloudflare IP range.

╔════════════════════════════════════════════════════════╗
║                    RESULT                              ║
╚════════════════════════════════════════════════════════╝

Detection score: 13
Result : HIGH CONFIDENCE
Status : Cloudflare is very likely being used.

Evidence:
  • DNS resolves to a known Cloudflare IP range.
  • HTTP Server header identifies Cloudflare.
  • Found 2 Cloudflare-specific HTTP header(s).
  • Socket resolution points to a known Cloudflare IP range.

------------------------------------------------------------
Note: Detection is based on observable indicators.
A website may use Cloudflare while hiding some indicators.
```

## Example Input (Non-Cloudflare)

```bash
python cloudflareCheck.py https://example.com
```

## Example Output (Not Detected)

```
╔════════════════════════════════════════════════════════╗
║         Cloudflare Detection Tool                      ║
╚════════════════════════════════════════════════════════╝

Target: https://example.com
Domain: example.com

[1] DNS Analysis
------------------------------------------------------------
A     : 93.184.216.34
AAAA  : 2606:2800:220:1:248:1893:25c8:1946
CNAME : Not found

[2] HTTP Analysis
------------------------------------------------------------
Final URL : https://example.com/
Status    : 200
Server    : ECS (nyc/1D34)

Cloudflare Headers:
  [-] No obvious Cloudflare headers found.

Cloudflare Cookies:
  [-] No obvious Cloudflare cookies found.

[3] Socket Resolution
------------------------------------------------------------
Resolved IP: 93.184.216.34
[-] IP is not in the known Cloudflare IPv4 ranges.

╔════════════════════════════════════════════════════════╗
║                    RESULT                              ║
╚════════════════════════════════════════════════════════╝

Detection score: 0
Result : NOT DETECTED
Status : No strong Cloudflare indicators were found.

------------------------------------------------------------
Note: Detection is based on observable indicators.
A website may use Cloudflare while hiding some indicators.
```

## How It Works

### Detection Scoring System

- **DNS IP Match** (+3 points): Domain resolves to Cloudflare IP ranges
- **DNS CNAME** (+3 points): CNAME record contains "cloudflare" or "cloudflare.net"
- **Cloudflare Headers** (+2 per header, max +6): CF-Ray, CF-Cache-Status, etc.
- **Server Header** (+4 points): Server header identifies Cloudflare
- **Cookies** (+2 points): Cloudflare-specific cookies detected
- **Socket Resolution** (+3 points): IP resolution matches Cloudflare ranges

### Confidence Levels

| Score | Result | Description |
|-------|--------|-------------|
| 7+ | **HIGH CONFIDENCE** | Cloudflare is very likely being used |
| 4-6 | **MEDIUM CONFIDENCE** | Several Cloudflare indicators detected |
| 2-3 | **LOW CONFIDENCE** | Some Cloudflare indicators detected |
| 0-1 | **NOT DETECTED** | No strong Cloudflare indicators found |

## Notes

- This tool uses heuristics and confidence scoring
- Some websites may use Cloudflare but hide certain indicators
- Results are best interpreted as a signal, not a guaranteed verdict
- Detection requires network connectivity to perform DNS and HTTP lookups

## License

MIT

## Author

Created by GH0STH4CKER
