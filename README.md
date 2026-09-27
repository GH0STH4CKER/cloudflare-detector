# 🔍 Cloudflare Detection Tool

[![GitHub](https://img.shields.io/badge/GitHub-GH0STH4CKER-blue?logo=github)](https://github.com/GH0STH4CKER/cloudflare-detector)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

A simple yet powerful Python script that checks whether a domain or URL is likely using Cloudflare by analyzing multiple detection vectors.

## ✨ Features

- 🌐 **DNS Analysis** - Checks A/AAAA/CNAME records against known Cloudflare IP ranges
- 📡 **HTTP Header Detection** - Scans for Cloudflare-specific response headers
- 🍪 **Cookie Analysis** - Identifies Cloudflare security cookies
- 🔌 **Socket Resolution** - Verifies IP addresses against Cloudflare IP blocks
- 📊 **Confidence Scoring** - Provides a reliability score based on multiple indicators
- 🎯 **Detailed Reports** - Beautiful formatted output with evidence breakdown

## ⚡ Quick Start

### 🌐 No Installation? Use Web Version!
  
**Don't want to download?** Try the web-based detector right now:

➡️ **[CloudPeek - Instant Cloudflare Detection](https://isitcloudflare.lovable.app/)**

Just paste a domain and get instant results! No installation required.

## 📋 Requirements

```bash
pip install requests dnspython
```

## 🚀 Quick Start

### Basic Usage

```bash
python cloudflareCheck.py example.com
```

### With Full URL

```bash
python cloudflareCheck.py https://example.com
```

### Get Help

```bash
python cloudflareCheck.py
```

## 📸 Example Output

### ✅ Cloudflare Detected (High Confidence)

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
Result : HIGH CONFIDENCE ✅
Status : Cloudflare is very likely being used.

Evidence:
  • DNS resolves to a known Cloudflare IP range.
  • HTTP Server header identifies Cloudflare.
  • Found 2 Cloudflare-specific HTTP header(s).
  • Socket resolution points to a known Cloudflare IP range.
```

### ❌ Not Detected

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
Result : NOT DETECTED ❌
Status : No strong Cloudflare indicators were found.
```

## 🔬 How It Works

### Detection Scoring System

| Indicator | Points | Description |
|-----------|--------|-------------|
| 🌐 DNS IP Match | +3 | Domain resolves to Cloudflare IP ranges |
| 🔗 DNS CNAME | +3 | CNAME contains "cloudflare" or "cloudflare.net" |
| 📬 Cloudflare Headers | +2 each (max +6) | CF-Ray, CF-Cache-Status, etc. |
| 🏷️ Server Header | +4 | Server header identifies Cloudflare |
| 🍪 Cookies | +2 | Cloudflare-specific cookies detected |
| 🔌 Socket IP | +3 | IP resolution matches Cloudflare ranges |

### Confidence Levels

| Score | Result | Badge | Description |
|-------|--------|-------|-------------|
| 7+ | **HIGH CONFIDENCE** | ✅ | Cloudflare is very likely being used |
| 4-6 | **MEDIUM CONFIDENCE** | ⚠️ | Several Cloudflare indicators detected |
| 2-3 | **LOW CONFIDENCE** | ℹ️ | Some Cloudflare indicators detected |
| 0-1 | **NOT DETECTED** | ❌ | No strong Cloudflare indicators found |

## 📊 Detection Methods

### 1️⃣ DNS Analysis
- Resolves domain A, AAAA, and CNAME records
- Compares resolved IPs against known Cloudflare IP ranges
- Identifies Cloudflare nameserver references

### 2️⃣ HTTP Header Analysis
- Checks for Cloudflare-specific response headers:
  - `CF-Ray` - Request tracking ID
  - `CF-Cache-Status` - Cache status
  - `CF-Mitigated` - Security status
  - And more...

### 3️⃣ Cookie Analysis
- Looks for Cloudflare cookies (`__cf*`, `cf_clearance`)
- Indicates active Cloudflare protection

### 4️⃣ Socket Resolution
- Performs direct socket lookup
- Verifies resolved IP against Cloudflare's IPv4 ranges

## ⚙️ Installation

### Clone Repository
```bash
git clone https://github.com/GH0STH4CKER/cloudflare-detector.git
cd cloudflare-detector
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install requests dnspython
```

## 🛠️ Advanced Usage

### Check Multiple Domains
```bash
for domain in example.com google.com cloudflare.com; do
    python cloudflareCheck.py $domain
done
```

### Save Results to File
```bash
python cloudflareCheck.py example.com > results.txt
```

## ⚠️ Important Notes

- **Heuristic-based**: Detection uses observable indicators and confidence scoring
- **Not Guaranteed**: Some websites may use Cloudflare while hiding certain indicators
- **Network Required**: Requires internet connectivity for DNS and HTTP lookups
- **Rate Limiting**: Don't check too many domains in rapid succession
- **Privacy**: Only performs DNS, HTTP, and socket lookups; no data collection

## 🔐 Security & Privacy

This tool:
- ✅ Does NOT store any data about checked domains
- ✅ Does NOT transmit results anywhere
- ✅ Only performs standard DNS and HTTP queries
- ✅ Runs entirely locally on your machine
- ✅ Can be audited by reading the source code

## 📝 Example Commands

```bash
# Check cloudflare.com
python cloudflareCheck.py cloudflare.com

# Check with HTTPS
python cloudflareCheck.py https://www.cloudflare.com

# Check GitHub
python cloudflareCheck.py github.com

# Check a subdomain
python cloudflareCheck.py api.example.com
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**GH0STH4CKER**
- GitHub: [@GH0STH4CKER](https://github.com/GH0STH4CKER)

## ⭐ Show Your Support

If you found this tool helpful, please consider:
- 🌟 Starring the repository
- 🔗 Sharing with others
- 💬 Providing feedback
- 🐛 Reporting issues

---

**Last Updated**: 2026-09-27  
**Status**: ✅ Active & Maintained
