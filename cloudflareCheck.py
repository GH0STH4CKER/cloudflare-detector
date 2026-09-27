import sys
import socket
import requests
import dns.resolver
from urllib.parse import urlparse


# Cloudflare IP ranges
CLOUDFLARE_IPV4_RANGES = [
    "173.245.48.0/20",
    "103.21.244.0/22",
    "103.22.200.0/22",
    "103.31.4.0/22",
    "141.101.64.0/18",
    "108.162.192.0/18",
    "190.93.240.0/20",
    "188.114.96.0/20",
    "197.234.240.0/22",
    "198.41.128.0/17",
    "162.158.0.0/15",
    "104.16.0.0/13",
    "104.24.0.0/14",
    "172.64.0.0/13",
    "131.0.72.0/22",
]

CLOUDFLARE_IPV6_RANGES = [
    "2400:cb00::/32",
    "2606:4700::/32",
    "2803:f800::/32",
    "2405:b500::/32",
    "2405:8100::/32",
    "2a06:98c0::/29",
    "2c0f:f248::/32",
]


def print_line():
    print("-" * 60)


def ip_in_network(ip, networks):
    import ipaddress

    try:
        ip_obj = ipaddress.ip_address(ip)

        for network in networks:
            if ip_obj in ipaddress.ip_network(network):
                return True

    except ValueError:
        pass

    return False


def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def get_dns_records(domain):
    records = {
        "A": [],
        "AAAA": [],
        "CNAME": []
    }

    for record_type in records:
        try:
            answers = dns.resolver.resolve(domain, record_type)

            for answer in answers:
                records[record_type].append(str(answer))

        except Exception:
            pass

    return records


def detect_cloudflare(url):
    url = normalize_url(url)

    parsed = urlparse(url)
    domain = parsed.hostname

    if not domain:
        print("Invalid URL.")
        return

    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " Cloudflare Detection Tool ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    print()
    print(f"Target: {url}")
    print(f"Domain: {domain}")
    print()

    score = 0
    reasons = []

    # ---------------------------------------------------------
    # DNS
    # ---------------------------------------------------------

    print("[1] DNS Analysis")
    print_line()

    dns_records = get_dns_records(domain)

    for record_type, values in dns_records.items():
        if values:
            print(f"{record_type:<6}: {', '.join(values)}")
        else:
            print(f"{record_type:<6}: Not found")

    # Check IPs
    all_ips = dns_records["A"] + dns_records["AAAA"]

    cloudflare_dns_ips = []

    for ip in all_ips:

        if ":" in ip:
            if ip_in_network(ip, CLOUDFLARE_IPV6_RANGES):
                cloudflare_dns_ips.append(ip)
        else:
            if ip_in_network(ip, CLOUDFLARE_IPV4_RANGES):
                cloudflare_dns_ips.append(ip)

    if cloudflare_dns_ips:
        score += 3

        reasons.append(
            "DNS resolves to a known Cloudflare IP range."
        )

        print()
        print("[+] Cloudflare IP detected")

    # Check CNAME
    cname_values = dns_records["CNAME"]

    if cname_values:

        for cname in cname_values:

            cname_lower = cname.lower()

            if (
                "cloudflare" in cname_lower
                or "cloudflare.net" in cname_lower
            ):
                score += 3

                reasons.append(
                    "DNS CNAME contains a Cloudflare hostname."
                )

                print("[+] Cloudflare CNAME detected")

    # ---------------------------------------------------------
    # HTTP
    # ---------------------------------------------------------

    print()
    print("[2] HTTP Analysis")
    print_line()

    try:

        response = requests.get(
            url,
            timeout=15,
            allow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/153.0 Safari/537.36"
                )
            }
        )

        print(f"Final URL : {response.url}")
        print(f"Status    : {response.status_code}")
        print(f"Server    : {response.headers.get('Server', 'Not present')}")

        # -----------------------------------------------------
        # Cloudflare headers
        # -----------------------------------------------------

        cf_headers = {
            "cf-ray": "CF-Ray",
            "cf-cache-status": "CF-Cache-Status",
            "cf-mitigated": "CF-Mitigated",
            "cf-chl-out": "CF-CHL-Out",
            "cf-apo-via": "CF-APO-Via",
            "cf-edge-cache": "CF-Edge-Cache",
        }

        print()
        print("Cloudflare Headers:")

        found_cf_headers = 0

        for header, display_name in cf_headers.items():

            if header in response.headers:

                value = response.headers.get(header)

                print(f"  [+] {display_name}: {value}")

                found_cf_headers += 1

        if found_cf_headers:
            score += min(found_cf_headers * 2, 6)

            reasons.append(
                f"Found {found_cf_headers} Cloudflare-specific HTTP header(s)."
            )

        else:
            print("  [-] No obvious Cloudflare headers found.")

        # -----------------------------------------------------
        # Server header
        # -----------------------------------------------------

        server = response.headers.get("Server", "").lower()

        if "cloudflare" in server:

            score += 4

            reasons.append(
                "HTTP Server header identifies Cloudflare."
            )

            print()
            print("[+] Server header indicates Cloudflare")

        # -----------------------------------------------------
        # Cookies
        # -----------------------------------------------------

        print()
        print("Cloudflare Cookies:")

        cf_cookies = []

        for cookie in response.cookies:

            cookie_name = cookie.name.lower()

            if cookie_name.startswith("__cf") or cookie_name in [
                "cf_clearance"
            ]:
                cf_cookies.append(cookie.name)

        if cf_cookies:

            score += 2

            reasons.append(
                "Cloudflare-specific cookie(s) detected."
            )

            for cookie in cf_cookies:
                print(f"  [+] {cookie}")

        else:
            print("  [-] No obvious Cloudflare cookies found.")

        # -----------------------------------------------------
        # Security headers / challenge
        # -----------------------------------------------------

        if "cf-ray" in response.headers:

            print()
            print("[+] CF-Ray request ID detected")

        if response.status_code in [403, 429, 503]:

            server_value = response.headers.get(
                "Server", ""
            ).lower()

            if (
                "cloudflare" in server_value
                or "cf-ray" in response.headers
            ):
                score += 2

                reasons.append(
                    "Response appears to be a Cloudflare security/challenge response."
                )

    except requests.RequestException as e:

        print(f"[!] HTTP request failed: {e}")

    # ---------------------------------------------------------
    # Socket IP
    # ---------------------------------------------------------

    print()
    print("[3] Socket Resolution")
    print_line()

    try:

        resolved_ip = socket.gethostbyname(domain)

        print(f"Resolved IP: {resolved_ip}")

        if ip_in_network(
            resolved_ip,
            CLOUDFLARE_IPV4_RANGES
        ):

            score += 3

            reasons.append(
                "Socket resolution points to a known Cloudflare IP range."
            )

            print("[+] IP belongs to a Cloudflare IP range.")

        else:
            print("[-] IP is not in the known Cloudflare IPv4 ranges.")

    except socket.gaierror as e:

        print(f"[!] Could not resolve domain: {e}")

    # ---------------------------------------------------------
    # Result
    # ---------------------------------------------------------

    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " RESULT ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    print()
    print(f"Detection score: {score}")

    if score >= 7:

        result = "HIGH CONFIDENCE"
        description = "Cloudflare is very likely being used."

    elif score >= 4:

        result = "MEDIUM CONFIDENCE"
        description = "Several Cloudflare indicators were detected."

    elif score >= 2:

        result = "LOW CONFIDENCE"
        description = "Some Cloudflare indicators were detected."

    else:

        result = "NOT DETECTED"
        description = "No strong Cloudflare indicators were found."

    print(f"Result : {result}")
    print(f"Status : {description}")

    if reasons:

        print()
        print("Evidence:")

        for reason in reasons:
            print(f"  • {reason}")

    print()
    print_line()
    print("Note: Detection is based on observable indicators.")
    print("A website may use Cloudflare while hiding some indicators.")
    print()


def main():

    if len(sys.argv) < 2:

        print()
        print("Usage:")
        print("  python cloudflareCheck.py example.com")
        print()
        print("Example:")
        print("  python cloudflareCheck.py https://example.com")
        print()

        sys.exit(1)

    target = sys.argv[1]

    detect_cloudflare(target)


if __name__ == "__main__":
    main()
