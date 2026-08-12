#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 ██╗   ██╗██████╗ ███╗   ██╗      ██╗  ██╗██╗███╗   ██╗ ██████╗
 ██║   ██║██╔══██╗████╗  ██║      ██║ ██╔╝██║████╗  ██║██╔════╝
 ██║   ██║██████╔╝██╔██╗ ██║█████╗█████╔╝ ██║██╔██╗ ██║██║  ███╗
 ╚██╗ ██╔╝██╔═══╝ ██║╚██╗██║╚════╝██╔═██╗ ██║██║╚██╗██║██║   ██║
  ╚████╔╝ ██║     ██║ ╚████║      ██║  ██╗██║██║ ╚████║╚██████╔╝
   ╚═══╝  ╚═╝     ╚═╝  ╚═══╝      ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝

           ⚡ VPN-KING SCANNER – BY DRAGON TECH ⚡
        Advanced Subdomain Recon & Network Analysis Tool
"""

import sys
import subprocess
import os
import hashlib
import getpass
import signal
import shutil
import stat
import socket
import ssl
import json
import time
import threading
import struct
import re

try:
    import urllib.request
    import urllib.error
    import urllib.parse
except ImportError:
    pass

# ---------- CTRL+C HANDLING ----------
def signal_handler(sig, frame):
    print(couleur("\n\n⚠️  Interruption detected. Returning to menu...", COULEURS.YELLOW))
    raise KeyboardInterrupt

signal.signal(signal.SIGINT, signal_handler)

# ---------- COLORS ----------
class COULEURS:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    GRAY = "\033[90m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

def couleur(text, code):
    return code + str(text) + COULEURS.RESET

# ---------- LOADING ANIMATION ----------
def loading_animation(message, stop_event):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write("\r" + couleur(frames[i % len(frames)] + " " + message, COULEURS.CYAN))
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 5) + "\r")
    sys.stdout.flush()

def start_loading(message):
    stop_event = threading.Event()
    t = threading.Thread(target=loading_animation, args=(message, stop_event), daemon=True)
    t.start()
    return stop_event

# ---------- HTTP REQUEST HELPER ----------
def http_get(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "VPN-KING-Scanner/1.0"})
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None

def http_get_json(url, timeout=10):
    data = http_get(url, timeout)
    if data:
        try:
            return json.loads(data)
        except:
            return None
    return None

def http_get_headers(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "VPN-KING-Scanner/1.0"})
        resp = urllib.request.urlopen(req, timeout=timeout)
        return dict(resp.headers), resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None, None

# ---------- AUTO INSTALLATION ----------
def is_installed():
    return shutil.which("vpnking") is not None

def install_script():
    print(couleur("\n🔧 FIRST USE – AUTOMATIC INSTALLATION", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("This tool will configure itself to run using the 'vpnking' command under ⚡DRAGON TECH⚡ framework.", COULEURS.BLUE))

    try:
        response = input(couleur("👉 Continue? (y/n): ", COULEURS.YELLOW)).strip().lower()
    except KeyboardInterrupt:
        print(couleur("\nInstallation cancelled. You can run it manually.", COULEURS.YELLOW))
        sys.exit(0)

    if response not in ("y", "yes"):
        print(couleur("Installation cancelled. Running in manual mode.", COULEURS.YELLOW))
        return

    bin_dir = os.path.expanduser("~/bin")
    os.makedirs(bin_dir, exist_ok=True)

    source = os.path.abspath(__file__)
    destination = os.path.join(bin_dir, "vpnking")

    try:
        shutil.copy2(source, destination)
        os.chmod(destination, os.stat(destination).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(couleur("✅ Script deployed to " + destination + " (⚡DRAGON TECH⚡ core)", COULEURS.GREEN))
    except Exception as e:
        print(couleur("❌ Deployment error: " + str(e), COULEURS.RED))
        return

    bashrc = os.path.expanduser("~/.bashrc")
    path_line = 'export PATH="$HOME/bin:$PATH"'

    try:
        with open(bashrc, "r") as f:
            content = f.read()
        if path_line not in content:
            with open(bashrc, "a") as f:
                f.write("\n# Added by ⚡DRAGON TECH⚡ VPN-KING SCANNER\n" + path_line + "\n")
            print(couleur("✅ PATH updated (⚡DRAGON TECH⚡ environment)", COULEURS.GREEN))
        else:
            print(couleur("ℹ️ PATH already configured.", COULEURS.BLUE))
    except Exception as e:
        print(couleur("⚠️ Cannot modify environment: " + str(e), COULEURS.YELLOW))

    alias_line = "alias vpnking='python ~/bin/vpnking'"
    try:
        with open(bashrc, "r") as f:
            content = f.read()
        if alias_line not in content:
            with open(bashrc, "a") as f:
                f.write(alias_line + "\n")
            print(couleur("✅ Alias added (⚡DRAGON TECH⚡ CLI)", COULEURS.GREEN))
    except:
        pass

    print(couleur("\n🎉 ⚡DRAGON TECH⚡ INSTALLATION COMPLETE!", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("Restart Termux or run:", COULEURS.BLUE))
    print(couleur("   source ~/.bashrc", COULEURS.YELLOW))
    print(couleur("Then run: vpnking", COULEURS.GREEN))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ---------- LOGO ----------
def show_logo():
    logo = """
""" + couleur("╔═══════════════════════════════════════════╗", COULEURS.YELLOW) + """
""" + couleur("║", COULEURS.YELLOW) + "  " + couleur("⚡ VPN-KING SCANNER – DRAGON TECH ⚡", COULEURS.GREEN + COULEURS.BOLD) + "  " + couleur("║", COULEURS.YELLOW) + """
""" + couleur("║", COULEURS.YELLOW) + "  " + couleur("  Advanced Recon & Network Intelligence  ", COULEURS.BLUE) + " " + couleur("║", COULEURS.YELLOW) + """
""" + couleur("║", COULEURS.YELLOW) + "  " + couleur("         Version 2.0 – ⚡DRAGON TECH⚡         ", COULEURS.GRAY) + couleur("║", COULEURS.YELLOW) + """
""" + couleur("╚═══════════════════════════════════════════╝", COULEURS.YELLOW)
    print(logo)

# ---------- PASSWORD SYSTEM ----------
PASSWORD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".dragontech_pass")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def set_default_password():
    with open(PASSWORD_FILE, "w") as f:
        f.write(hash_password("tdftech"))

def verify_password():
    if not os.path.exists(PASSWORD_FILE):
        set_default_password()
    with open(PASSWORD_FILE, "r") as f:
        stored_hash = f.read().strip()
    attempts = 3
    while attempts > 0:
        try:
            password = getpass.getpass(couleur("🔑 ⚡DRAGON TECH⚡ Password: ", COULEURS.YELLOW))
        except KeyboardInterrupt:
            print(couleur("\n👋 Exiting ⚡DRAGON TECH⚡ system...", COULEURS.GREEN))
            sys.exit(0)
        if hash_password(password) == stored_hash:
            print(couleur("✅ ⚡DRAGON TECH⚡ Access Granted.", COULEURS.GREEN))
            return True
        else:
            attempts -= 1
            print(couleur("❌ Incorrect password. " + str(attempts) + " attempt(s) remaining.", COULEURS.RED))
    print(couleur("🚫 ⚡DRAGON TECH⚡ Access Denied.", COULEURS.RED))
    sys.exit(1)

def change_password():
    print(couleur("\n🔐 ⚡DRAGON TECH⚡ Password Change", COULEURS.BLUE))
    try:
        old = getpass.getpass(couleur("Old password: ", COULEURS.YELLOW))
    except KeyboardInterrupt:
        print(couleur("\nCancelled.", COULEURS.YELLOW))
        return
    with open(PASSWORD_FILE, "r") as f:
        if hash_password(old) != f.read().strip():
            print(couleur("❌ Incorrect old password.", COULEURS.RED))
            return
    try:
        new_pass = getpass.getpass(couleur("New password: ", COULEURS.YELLOW))
        confirm = getpass.getpass(couleur("Confirm password: ", COULEURS.YELLOW))
    except KeyboardInterrupt:
        print(couleur("\nCancelled.", COULEURS.YELLOW))
        return
    if new_pass != confirm:
        print(couleur("❌ Password mismatch.", COULEURS.RED))
        return
    with open(PASSWORD_FILE, "w") as f:
        f.write(hash_password(new_pass))
    print(couleur("✅ ⚡DRAGON TECH⚡ password updated successfully.", COULEURS.GREEN))

# ---------- COMMON SUBDOMAINS WORDLIST ----------
COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "ns2",
    "dns", "dns1", "dns2", "mx", "mx1", "mx2", "blog", "dev", "staging", "api",
    "app", "admin", "portal", "test", "vpn", "cdn", "cloud", "git", "svn",
    "ssh", "remote", "server", "web", "email", "secure", "shop", "store",
    "forum", "wiki", "docs", "support", "help", "status", "monitor", "beta",
    "alpha", "demo", "sandbox", "proxy", "gateway", "firewall", "backup",
    "db", "database", "mysql", "postgres", "redis", "mongo", "elastic",
    "search", "media", "img", "images", "static", "assets", "files", "download",
    "upload", "video", "stream", "live", "chat", "irc", "jabber", "xmpp",
    "calendar", "crm", "erp", "hr", "intranet", "internal", "private",
    "public", "mobile", "m", "wap", "imap", "pop3", "cpanel", "whm",
    "webdisk", "autodiscover", "autoconfig", "owa", "exchange", "relay",
    "ns3", "ns4", "dns3", "dns4", "mx3", "mail2", "mail3", "smtp2",
    "dev1", "dev2", "stage", "staging2", "qa", "uat", "prod", "production",
    "jenkins", "ci", "cd", "docker", "k8s", "kubernetes", "grafana",
    "prometheus", "kibana", "logstash", "sentry", "vault", "consul",
    "registry", "repo", "nexus", "artifactory", "sonar", "jira", "confluence"
]

# ========== TOOL 1: SUBDOMAIN SCANNER ==========
def subdomain_scanner():
    print(couleur("\n🔍 SUBDOMAIN SCANNER", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        domain = input(couleur("Enter target domain (e.g. example.com): ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not domain:
        print(couleur("❌ No domain provided.", COULEURS.RED))
        return

    print(couleur("\nScanning subdomains for: " + domain, COULEURS.BLUE))
    found = []
    total = len(COMMON_SUBDOMAINS)

    for i, sub in enumerate(COMMON_SUBDOMAINS):
        target = sub + "." + domain
        progress = int((i + 1) / total * 100)
        sys.stdout.write("\r" + couleur("  Progress: [" + "█" * (progress // 5) + "░" * (20 - progress // 5) + "] " + str(progress) + "% - Testing: " + target, COULEURS.CYAN))
        sys.stdout.flush()
        try:
            ip = socket.gethostbyname(target)
            found.append((target, ip))
        except socket.gaierror:
            pass
        except Exception:
            pass

    print("\n")
    if found:
        print(couleur("✅ Found " + str(len(found)) + " subdomain(s):\n", COULEURS.GREEN))
        print(couleur("  {:<40} {}".format("SUBDOMAIN", "IP ADDRESS"), COULEURS.BOLD + COULEURS.WHITE))
        print(couleur("  " + "─" * 60, COULEURS.GRAY))
        for sub, ip in found:
            print(couleur("  {:<40} {}".format(sub, ip), COULEURS.CYAN))
    else:
        print(couleur("⚠️ No subdomains found.", COULEURS.YELLOW))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== TOOL 2: PORT SCANNER ==========
def port_scanner():
    print(couleur("\n🔌 PORT SCANNER", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        target = input(couleur("Enter target IP or domain: ", COULEURS.YELLOW)).strip()
        port_range = input(couleur("Port range (e.g. 1-1024, default: common ports): ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not target:
        print(couleur("❌ No target provided.", COULEURS.RED))
        return

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(couleur("❌ Cannot resolve: " + target, COULEURS.RED))
        return

    common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
                    993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443, 8888, 27017]

    if port_range and "-" in port_range:
        try:
            parts = port_range.split("-")
            start_port = int(parts[0])
            end_port = int(parts[1])
            ports = list(range(start_port, end_port + 1))
        except:
            print(couleur("⚠️ Invalid range. Using common ports.", COULEURS.YELLOW))
            ports = common_ports
    else:
        ports = common_ports

    print(couleur("\nScanning " + ip + " (" + target + ") - " + str(len(ports)) + " ports...\n", COULEURS.BLUE))
    open_ports = []
    total = len(ports)

    for i, port in enumerate(ports):
        progress = int((i + 1) / total * 100)
        sys.stdout.write("\r" + couleur("  Progress: [" + "█" * (progress // 5) + "░" * (20 - progress // 5) + "] " + str(progress) + "% - Port: " + str(port), COULEURS.CYAN))
        sys.stdout.flush()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = get_service_name(port)
                open_ports.append((port, service))
            sock.close()
        except:
            pass

    print("\n")
    if open_ports:
        print(couleur("✅ Found " + str(len(open_ports)) + " open port(s):\n", COULEURS.GREEN))
        print(couleur("  {:<10} {:<15} {}".format("PORT", "STATE", "SERVICE"), COULEURS.BOLD + COULEURS.WHITE))
        print(couleur("  " + "─" * 40, COULEURS.GRAY))
        for port, service in open_ports:
            print(couleur("  {:<10} {:<15} {}".format(str(port), "OPEN", service), COULEURS.CYAN))
    else:
        print(couleur("⚠️ No open ports found.", COULEURS.YELLOW))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

def get_service_name(port):
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 111: "RPCBind", 135: "MSRPC",
        139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
        993: "IMAPS", 995: "POP3S", 1723: "PPTP", 3306: "MySQL",
        3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Proxy",
        8443: "HTTPS-Alt", 8888: "HTTP-Alt", 27017: "MongoDB"
    }
    return services.get(port, "Unknown")

# ========== TOOL 3: IP LOOKUP / WHOIS ==========
def ip_lookup():
    print(couleur("\n🌍 IP LOOKUP / WHOIS", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        target = input(couleur("Enter IP address or domain: ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not target:
        print(couleur("❌ No target provided.", COULEURS.RED))
        return

    stop = start_loading("Looking up IP information...")
    data = http_get_json("http://ip-api.com/json/" + target + "?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
    stop.set()

    if data and data.get("status") == "success":
        print(couleur("\n✅ IP Information:\n", COULEURS.GREEN))
        fields = [
            ("IP Address", data.get("query", "N/A")),
            ("Country", data.get("country", "N/A") + " (" + data.get("countryCode", "") + ")"),
            ("Region", data.get("regionName", "N/A")),
            ("City", data.get("city", "N/A")),
            ("ZIP Code", data.get("zip", "N/A")),
            ("Latitude", str(data.get("lat", "N/A"))),
            ("Longitude", str(data.get("lon", "N/A"))),
            ("Timezone", data.get("timezone", "N/A")),
            ("ISP", data.get("isp", "N/A")),
            ("Organization", data.get("org", "N/A")),
            ("AS Number", data.get("as", "N/A")),
        ]
        for label, value in fields:
            print(couleur("  {:<15} : {}".format(label, value), COULEURS.CYAN))
    else:
        msg = data.get("message", "Unknown error") if data else "Connection failed"
        print(couleur("❌ Lookup failed: " + msg, COULEURS.RED))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== TOOL 4: DNS LOOKUP ==========
def dns_lookup():
    print(couleur("\n📡 DNS LOOKUP", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        domain = input(couleur("Enter domain: ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not domain:
        print(couleur("❌ No domain provided.", COULEURS.RED))
        return

    stop = start_loading("Querying DNS records...")

    records = {}
    # A Record
    try:
        ips = socket.getaddrinfo(domain, None, socket.AF_INET)
        records["A"] = list(set([ip[4][0] for ip in ips]))
    except:
        records["A"] = []

    # AAAA Record
    try:
        ips = socket.getaddrinfo(domain, None, socket.AF_INET6)
        records["AAAA"] = list(set([ip[4][0] for ip in ips]))
    except:
        records["AAAA"] = []

    # Use DNS over HTTPS for MX, NS, TXT, CNAME
    for rtype in ["MX", "NS", "TXT", "CNAME"]:
        data = http_get_json("https://dns.google/resolve?name=" + domain + "&type=" + rtype)
        if data and "Answer" in data:
            records[rtype] = [a.get("data", "") for a in data["Answer"]]
        else:
            records[rtype] = []

    stop.set()

    print(couleur("\n✅ DNS Records for: " + domain + "\n", COULEURS.GREEN))
    for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]:
        vals = records.get(rtype, [])
        if vals:
            print(couleur("  " + rtype + " Records:", COULEURS.BOLD + COULEURS.WHITE))
            for v in vals:
                print(couleur("    → " + v, COULEURS.CYAN))
        else:
            print(couleur("  " + rtype + " Records:", COULEURS.BOLD + COULEURS.WHITE))
            print(couleur("    → None found", COULEURS.GRAY))
        print()
    input(couleur("Press Enter to continue...", COULEURS.GRAY))

# ========== TOOL 5: REVERSE IP LOOKUP ==========
def reverse_ip_lookup():
    print(couleur("\n🔄 REVERSE IP LOOKUP", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        target = input(couleur("Enter IP address: ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not target:
        print(couleur("❌ No target provided.", COULEURS.RED))
        return

    stop = start_loading("Looking up reverse DNS...")

    results = []
    try:
        hostname, aliases, addresses = socket.gethostbyaddr(target)
        results.append(hostname)
        results.extend(aliases)
    except:
        pass

    # Try additional API
    data = http_get_json("https://dns.google/resolve?name=" + ".".join(reversed(target.split("."))) + ".in-addr.arpa&type=PTR")
    if data and "Answer" in data:
        for a in data["Answer"]:
            name = a.get("data", "").rstrip(".")
            if name and name not in results:
                results.append(name)

    stop.set()

    if results:
        print(couleur("\n✅ Domains found on " + target + ":\n", COULEURS.GREEN))
        for r in results:
            print(couleur("  → " + r, COULEURS.CYAN))
    else:
        print(couleur("\n⚠️ No reverse DNS records found for " + target, COULEURS.YELLOW))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== TOOL 6: WEBSITE TECHNOLOGY DETECTION ==========
def tech_detection():
    print(couleur("\n🛠️ WEBSITE TECHNOLOGY DETECTION", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        url = input(couleur("Enter URL (e.g. https://example.com): ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not url:
        print(couleur("❌ No URL provided.", COULEURS.RED))
        return
    if not url.startswith("http"):
        url = "https://" + url

    stop = start_loading("Detecting technologies...")
    headers, body = http_get_headers(url)
    stop.set()

    if not headers:
        print(couleur("❌ Could not connect to " + url, COULEURS.RED))
        input(couleur("\nPress Enter to continue...", COULEURS.GRAY))
        return

    techs = []

    # Server
    server = headers.get("Server", headers.get("server", ""))
    if server:
        techs.append(("Web Server", server))

    # X-Powered-By
    powered = headers.get("X-Powered-By", headers.get("x-powered-by", ""))
    if powered:
        techs.append(("Powered By", powered))

    # Content-Type
    ct = headers.get("Content-Type", headers.get("content-type", ""))
    if ct:
        techs.append(("Content-Type", ct))

    if body:
        body_lower = body.lower()
        # CMS Detection
        if "wp-content" in body_lower or "wordpress" in body_lower:
            techs.append(("CMS", "WordPress"))
        elif "joomla" in body_lower:
            techs.append(("CMS", "Joomla"))
        elif "drupal" in body_lower:
            techs.append(("CMS", "Drupal"))
        elif "shopify" in body_lower:
            techs.append(("Platform", "Shopify"))
        elif "squarespace" in body_lower:
            techs.append(("Platform", "Squarespace"))
        elif "wix.com" in body_lower:
            techs.append(("Platform", "Wix"))

        # JS Frameworks
        if "react" in body_lower or "_next" in body_lower or "__next" in body_lower:
            techs.append(("JS Framework", "React / Next.js"))
        if "vue" in body_lower or "nuxt" in body_lower:
            techs.append(("JS Framework", "Vue.js / Nuxt"))
        if "angular" in body_lower:
            techs.append(("JS Framework", "Angular"))
        if "jquery" in body_lower:
            techs.append(("JS Library", "jQuery"))
        if "bootstrap" in body_lower:
            techs.append(("CSS Framework", "Bootstrap"))
        if "tailwind" in body_lower:
            techs.append(("CSS Framework", "Tailwind CSS"))

        # Analytics
        if "google-analytics" in body_lower or "gtag" in body_lower or "ga.js" in body_lower:
            techs.append(("Analytics", "Google Analytics"))
        if "facebook" in body_lower and "pixel" in body_lower:
            techs.append(("Analytics", "Facebook Pixel"))

        # CDN
        if "cloudflare" in body_lower:
            techs.append(("CDN", "Cloudflare"))
        if "cloudfront" in body_lower:
            techs.append(("CDN", "AWS CloudFront"))
        if "akamai" in body_lower:
            techs.append(("CDN", "Akamai"))

    # Check headers for CDN
    cf_ray = headers.get("CF-RAY", headers.get("cf-ray", ""))
    if cf_ray:
        techs.append(("CDN", "Cloudflare (CF-RAY: " + cf_ray + ")"))

    print(couleur("\n✅ Technologies detected on " + url + ":\n", COULEURS.GREEN))
    if techs:
        print(couleur("  {:<20} {}".format("CATEGORY", "TECHNOLOGY"), COULEURS.BOLD + COULEURS.WHITE))
        print(couleur("  " + "─" * 50, COULEURS.GRAY))
        for cat, tech in techs:
            print(couleur("  {:<20} {}".format(cat, tech), COULEURS.CYAN))
    else:
        print(couleur("  ⚠️ No technologies detected.", COULEURS.YELLOW))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== TOOL 7: NETWORK INFO ==========
def network_info():
    print(couleur("\n📶 NETWORK INFORMATION", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))

    stop = start_loading("Gathering network info...")

    info = []

    # Local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        info.append(("Local IP", local_ip))
    except:
        info.append(("Local IP", "Unable to detect"))

    # Public IP
    public_ip = http_get("https://api.ipify.org")
    if public_ip:
        info.append(("Public IP", public_ip.strip()))
    else:
        info.append(("Public IP", "Unable to detect"))

    # Hostname
    try:
        info.append(("Hostname", socket.gethostname()))
    except:
        info.append(("Hostname", "Unknown"))

    # DNS Servers (try resolv.conf)
    try:
        with open("/etc/resolv.conf", "r") as f:
            for line in f:
                if line.strip().startswith("nameserver"):
                    info.append(("DNS Server", line.strip().split()[1]))
    except:
        # Try Termux/Android approach
        try:
            result = subprocess.run(["getprop", "net.dns1"], capture_output=True, text=True, timeout=5)
            if result.stdout.strip():
                info.append(("DNS Server", result.stdout.strip()))
        except:
            pass

    stop.set()

    print(couleur("\n✅ Network Information:\n", COULEURS.GREEN))
    for label, value in info:
        print(couleur("  {:<15} : {}".format(label, value), COULEURS.CYAN))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== TOOL 8: PING SWEEP ==========
def ping_sweep():
    print(couleur("\n📡 PING SWEEP", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        network = input(couleur("Enter network (e.g. 192.168.1): ", COULEURS.YELLOW)).strip()
        range_input = input(couleur("Host range (e.g. 1-254, default: 1-254): ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not network:
        print(couleur("❌ No network provided.", COULEURS.RED))
        return

    if range_input and "-" in range_input:
        try:
            parts = range_input.split("-")
            start = int(parts[0])
            end = int(parts[1])
        except:
            start, end = 1, 254
    else:
        start, end = 1, 254

    print(couleur("\nSweeping " + network + "." + str(start) + " - " + network + "." + str(end) + "...\n", COULEURS.BLUE))
    alive = []
    total = end - start + 1

    for i, host_num in enumerate(range(start, end + 1)):
        ip = network + "." + str(host_num)
        progress = int((i + 1) / total * 100)
        sys.stdout.write("\r" + couleur("  Progress: [" + "█" * (progress // 5) + "░" * (20 - progress // 5) + "] " + str(progress) + "% - Pinging: " + ip, COULEURS.CYAN))
        sys.stdout.flush()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, 80))
            if result == 0:
                alive.append(ip)
            sock.close()
        except:
            pass
        # Also try port 443
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, 443))
            if result == 0 and ip not in alive:
                alive.append(ip)
            sock.close()
        except:
            pass

    print("\n")
    if alive:
        print(couleur("✅ Found " + str(len(alive)) + " live host(s):\n", COULEURS.GREEN))
        for ip in alive:
            print(couleur("  🟢 " + ip, COULEURS.CYAN))
    else:
        print(couleur("⚠️ No live hosts found.", COULEURS.YELLOW))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== TOOL 9: BANNER GRABBING ==========
def banner_grabbing():
    print(couleur("\n🏴 BANNER GRABBING", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        target = input(couleur("Enter target IP or domain: ", COULEURS.YELLOW)).strip()
        port_input = input(couleur("Enter port (default: 80): ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not target:
        print(couleur("❌ No target provided.", COULEURS.RED))
        return

    port = int(port_input) if port_input.isdigit() else 80

    stop = start_loading("Grabbing banner from " + target + ":" + str(port) + "...")

    banner = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target, port))
        # Send HTTP request for web ports
        if port in [80, 8080, 8888, 443, 8443]:
            sock.send(("HEAD / HTTP/1.1\r\nHost: " + target + "\r\n\r\n").encode())
        else:
            sock.send(b"\r\n")
        banner = sock.recv(4096).decode("utf-8", errors="replace")
        sock.close()
    except Exception as e:
        banner = "Error: " + str(e)

    stop.set()

    print(couleur("\n✅ Banner from " + target + ":" + str(port) + ":\n", COULEURS.GREEN))
    if banner:
        for line in banner.split("\n")[:20]:
            print(couleur("  " + line.rstrip(), COULEURS.CYAN))
    else:
        print(couleur("  ⚠️ No banner received.", COULEURS.YELLOW))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== TOOL 10: HTTP HEADER ANALYSIS ==========
def http_header_analysis():
    print(couleur("\n🔒 HTTP HEADER ANALYSIS", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        url = input(couleur("Enter URL (e.g. https://example.com): ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not url:
        print(couleur("❌ No URL provided.", COULEURS.RED))
        return
    if not url.startswith("http"):
        url = "https://" + url

    stop = start_loading("Analyzing HTTP headers...")
    headers, _ = http_get_headers(url)
    stop.set()

    if not headers:
        print(couleur("❌ Could not connect to " + url, COULEURS.RED))
        input(couleur("\nPress Enter to continue...", COULEURS.GRAY))
        return

    print(couleur("\n✅ HTTP Headers for " + url + ":\n", COULEURS.GREEN))
    print(couleur("  {:<35} {}".format("HEADER", "VALUE"), COULEURS.BOLD + COULEURS.WHITE))
    print(couleur("  " + "─" * 70, COULEURS.GRAY))
    for key, value in headers.items():
        print(couleur("  {:<35} {}".format(key, value), COULEURS.CYAN))

    # Security analysis
    print(couleur("\n  🛡️ Security Header Analysis:", COULEURS.BOLD + COULEURS.WHITE))
    print(couleur("  " + "─" * 50, COULEURS.GRAY))

    security_headers = {
        "Strict-Transport-Security": "HSTS - Forces HTTPS",
        "Content-Security-Policy": "CSP - Prevents XSS",
        "X-Frame-Options": "Clickjacking Protection",
        "X-Content-Type-Options": "MIME Sniffing Protection",
        "X-XSS-Protection": "XSS Filter",
        "Referrer-Policy": "Referrer Control",
        "Permissions-Policy": "Feature Permissions",
    }

    headers_lower = {k.lower(): v for k, v in headers.items()}
    for header, description in security_headers.items():
        if header.lower() in headers_lower:
            print(couleur("  ✅ " + header + " - " + description, COULEURS.GREEN))
        else:
            print(couleur("  ❌ " + header + " - " + description + " (MISSING)", COULEURS.RED))

    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== TOOL 11: SSL/TLS CERTIFICATE INFO ==========
def ssl_certificate_info():
    print(couleur("\n🔐 SSL/TLS CERTIFICATE INFO", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("━" * 40, COULEURS.GRAY))
    try:
        domain = input(couleur("Enter domain (e.g. example.com): ", COULEURS.YELLOW)).strip()
    except KeyboardInterrupt:
        return
    if not domain:
        print(couleur("❌ No domain provided.", COULEURS.RED))
        return

    stop = start_loading("Fetching SSL certificate...")

    cert_info = None
    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
        conn.settimeout(10)
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        conn.close()
        cert_info = cert
    except Exception as e:
        stop.set()
        print(couleur("\n❌ SSL Error: " + str(e), COULEURS.RED))
        input(couleur("\nPress Enter to continue...", COULEURS.GRAY))
        return

    stop.set()

    if cert_info:
        print(couleur("\n✅ SSL Certificate for " + domain + ":\n", COULEURS.GREEN))

        # Subject
        subject = dict(x[0] for x in cert_info.get("subject", []))
        issuer = dict(x[0] for x in cert_info.get("issuer", []))

        fields = [
            ("Common Name", subject.get("commonName", "N/A")),
            ("Organization", subject.get("organizationName", "N/A")),
            ("Issuer", issuer.get("organizationName", "N/A")),
            ("Issuer CN", issuer.get("commonName", "N/A")),
            ("Valid From", cert_info.get("notBefore", "N/A")),
            ("Valid Until", cert_info.get("notAfter", "N/A")),
            ("Serial Number", cert_info.get("serialNumber", "N/A")),
            ("Version", str(cert_info.get("version", "N/A"))),
        ]

        for label, value in fields:
            print(couleur("  {:<15} : {}".format(label, value), COULEURS.CYAN))

        # SANs
        sans = cert_info.get("subjectAltName", [])
        if sans:
            print(couleur("\n  Subject Alt Names:", COULEURS.BOLD + COULEURS.WHITE))
            for san_type, san_value in sans[:10]:
                print(couleur("    → " + san_value, COULEURS.CYAN))
            if len(sans) > 10:
                print(couleur("    ... and " + str(len(sans) - 10) + " more", COULEURS.GRAY))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== MAIN MENU ==========
def show_menu():
    print()
    print(couleur("  ┌─────────────────────────────────────┐", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("        ⚡ DRAGON TECH MAIN MENU ⚡         ", COULEURS.GREEN + COULEURS.BOLD) + couleur("│", COULEURS.YELLOW))
    print(couleur("  ├─────────────────────────────────────┤", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [01] Subdomain Scanner              ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [02] Port Scanner                   ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [03] IP Lookup / WHOIS              ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [04] DNS Lookup                     ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [05] Reverse IP Lookup              ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [06] Website Tech Detection         ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [07] Network Info                   ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [08] Ping Sweep                     ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [09] Banner Grabbing                ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [10] HTTP Header Analysis           ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [11] SSL/TLS Certificate Info       ", COULEURS.CYAN) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [12] Change Password                ", COULEURS.MAGENTA) + couleur("│", COULEURS.YELLOW))
    print(couleur("  │", COULEURS.YELLOW) + couleur("  [00] Exit                           ", COULEURS.RED) + couleur("│", COULEURS.YELLOW))
    print(couleur("  └─────────────────────────────────────┘", COULEURS.YELLOW))

def main():
    os.system("clear" if os.name != "nt" else "cls")
    show_logo()

    # Auto-install on first run
    if not is_installed():
        install_script()

    # Password verification
    verify_password()

    while True:
        try:
            show_menu()
            choice = input(couleur("\n  ⚡ DRAGON TECH > ", COULEURS.GREEN + COULEURS.BOLD)).strip()

            if choice == "1" or choice == "01":
                subdomain_scanner()
            elif choice == "2" or choice == "02":
                port_scanner()
            elif choice == "3" or choice == "03":
                ip_lookup()
            elif choice == "4" or choice == "04":
                dns_lookup()
            elif choice == "5" or choice == "05":
                reverse_ip_lookup()
            elif choice == "6" or choice == "06":
                tech_detection()
            elif choice == "7" or choice == "07":
                network_info()
            elif choice == "8" or choice == "08":
                ping_sweep()
            elif choice == "9" or choice == "09":
                banner_grabbing()
            elif choice == "10":
                http_header_analysis()
            elif choice == "11":
                ssl_certificate_info()
            elif choice == "12":
                change_password()
            if choice == "9" or choice == "09":
    print("""
╔══════════════════════════════════════╗
║          BANNER GRABBING             ║
╠══════════════════════════════════════╣
║  1 • Basic Banner                    ║
║  2 • HTTP Banner                     ║
║  3 • HTTPS Banner                    ║
║  4 • Service Information             ║
║  5 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("BANNER > ").strip()

    if sub_choice == "1":
        basic_banner_check()
    elif sub_choice == "2":
        http_banner_check()
    elif sub_choice == "3":
        https_banner_check()
    elif sub_choice == "4":
        service_information()

elif choice == "10" or choice == "010":
    print("""
╔══════════════════════════════════════╗
║          HTTP HEADERS                ║
╠══════════════════════════════════════╣
║  1 • Request Headers                 ║
║  2 • Response Headers                ║
║  3 • Security Headers                ║
║  4 • Redirect Check                  ║
║  5 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("HEADERS > ").strip()

    if sub_choice == "1":
        request_headers()
    elif sub_choice == "2":
        response_headers()
    elif sub_choice == "3":
        security_headers()
    elif sub_choice == "4":
        redirect_check()

elif choice == "11" or choice == "011":
    print("""
╔══════════════════════════════════════╗
║             SSL / TLS                ║
╠══════════════════════════════════════╣
║  1 • Certificate Information         ║
║  2 • TLS Information                 ║
║  3 • Certificate Expiry              ║
║  4 • Cipher Information              ║
║  5 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("SSL > ").strip()

    if sub_choice == "1":
        certificate_information()
    elif sub_choice == "2":
        tls_information()
    elif sub_choice == "3":
        certificate_expiration()
    elif sub_choice == "4":
        cipher_information()

elif choice == "12" or choice == "012":
    print("""
╔══════════════════════════════════════╗
║          PASSWORD TOOLS              ║
╠══════════════════════════════════════╣
║  1 • Change Password                 ║
║  2 • Generate Password               ║
║  3 • Password Strength               ║
║  4 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("PASSWORD > ").strip()

    if sub_choice == "1":
        change_password()
    elif sub_choice == "2":
        generate_password()
    elif sub_choice == "3":
        password_strength()

elif choice == "13" or choice == "013":
    print("""
╔══════════════════════════════════════╗
║            DNS RECORDS               ║
╠══════════════════════════════════════╣
║  1 • A Record                        ║
║  2 • AAAA Record                    ║
║  3 • MX Record                      ║
║  4 • NS Record                      ║
║  5 • TXT Record                     ║
║  6 • CNAME Record                   ║
║  7 • All Records                    ║
║  8 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("DNS > ").strip()

    if sub_choice == "1":
        dns_a_record()
    elif sub_choice == "2":
        dns_aaaa_record()
    elif sub_choice == "3":
        dns_mx_record()
    elif sub_choice == "4":
        dns_ns_record()
    elif sub_choice == "5":
        dns_txt_record()
    elif sub_choice == "6":
        dns_cname_record()
    elif sub_choice == "7":
        dns_all_records()

elif choice == "14" or choice == "014":
    print("""
╔══════════════════════════════════════╗
║          REVERSE DNS                 ║
╠══════════════════════════════════════╣
║  1 • Reverse Lookup                  ║
║  2 • Hostname Lookup                 ║
║  3 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("REVERSE DNS > ").strip()

    if sub_choice == "1":
        reverse_lookup()
    elif sub_choice == "2":
        hostname_lookup()

elif choice == "15" or choice == "015":
    print("""
╔══════════════════════════════════════╗
║              WHOIS                   ║
╠══════════════════════════════════════╣
║  1 • Domain WHOIS                    ║
║  2 • IP WHOIS                        ║
║  3 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("WHOIS > ").strip()

    if sub_choice == "1":
        domain_whois()
    elif sub_choice == "2":
        ip_whois()

elif choice == "16" or choice == "016":
    print("""
╔══════════════════════════════════════╗
║          IP GEOLOCATION              ║
╠══════════════════════════════════════╣
║  1 • Country                         ║
║  2 • City                            ║
║  3 • ISP                             ║
║  4 • ASN                             ║
║  5 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("GEO > ").strip()

    if sub_choice == "1":
        ip_country()
    elif sub_choice == "2":
        ip_city()
    elif sub_choice == "3":
        ip_isp()
    elif sub_choice == "4":
        ip_asn()

elif choice == "17" or choice == "017":
    print("""
╔══════════════════════════════════════╗
║              PING                    ║
╠══════════════════════════════════════╣
║  1 • Single Ping                     ║
║  2 • Connectivity Test               ║
║  3 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("PING > ").strip()

    if sub_choice == "1":
        single_ping()
    elif sub_choice == "2":
        ping_connectivity()

elif choice == "18" or choice == "018":
    print("""
╔══════════════════════════════════════╗
║           TRACEROUTE                 ║
╠══════════════════════════════════════╣
║  1 • IPv4                            ║
║  2 • IPv6                            ║
║  3 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("TRACE > ").strip()

    if sub_choice == "1":
        traceroute_ipv4()
    elif sub_choice == "2":
        traceroute_ipv6()

elif choice == "19" or choice == "019":
    print("""
╔══════════════════════════════════════╗
║           HTTP STATUS                ║
╠══════════════════════════════════════╣
║  1 • HTTP Status                     ║
║  2 • HTTPS Status                    ║
║  3 • Redirect Check                  ║
║  4 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("STATUS > ").strip()

    if sub_choice == "1":
        http_status()
    elif sub_choice == "2":
        https_status()
    elif sub_choice == "3":
        redirect_check()

elif choice == "20" or choice == "020":
    print("""
╔══════════════════════════════════════╗
║        NETWORK INFORMATION           ║
╠══════════════════════════════════════╣
║  1 • Interfaces                      ║
║  2 • Routing Table                   ║
║  3 • DNS Configuration               ║
║  4 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("NETWORK > ").strip()

    if sub_choice == "1":
        network_interfaces()
    elif sub_choice == "2":
        routing_table()
    elif sub_choice == "3":
        dns_configuration()

elif choice == "21" or choice == "021":
    print("""
╔══════════════════════════════════════╗
║          SUBDOMAIN TOOLS             ║
╠══════════════════════════════════════╣
║  1 • Basic Enumeration               ║
║  2 • DNS Enumeration                 ║
║  3 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("SUBDOMAIN > ").strip()

    if sub_choice == "1":
        basic_subdomain_scan()
    elif sub_choice == "2":
        dns_subdomain_scan()

elif choice == "22" or choice == "022":
    print("""
╔══════════════════════════════════════╗
║         DOMAIN INFORMATION           ║
╠══════════════════════════════════════╣
║  1 • Domain Info                     ║
║  2 • DNS Info                        ║
║  3 • Registration Info               ║
║  4 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("DOMAIN > ").strip()

    if sub_choice == "1":
        domain_info()
    elif sub_choice == "2":
        domain_dns_info()
    elif sub_choice == "3":
        registration_info()

elif choice == "23" or choice == "023":
    print("""
╔══════════════════════════════════════╗
║             LOCAL IP                 ║
╠══════════════════════════════════════╣
║  1 • IPv4                            ║
║  2 • IPv6                            ║
║  3 • Gateway                         ║
║  4 • Interfaces                      ║
║  5 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("LOCAL IP > ").strip()

    if sub_choice == "1":
        local_ipv4()
    elif sub_choice == "2":
        local_ipv6()
    elif sub_choice == "3":
        local_gateway()
    elif sub_choice == "4":
        local_interfaces()

elif choice == "24" or choice == "024":
    print("""
╔══════════════════════════════════════╗
║             PUBLIC IP                ║
╠══════════════════════════════════════╣
║  1 • Public IPv4                     ║
║  2 • Public IPv6                     ║
║  3 • IP Information                  ║
║  4 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("PUBLIC IP > ").strip()

    if sub_choice == "1":
        public_ipv4()
    elif sub_choice == "2":
        public_ipv6()
    elif sub_choice == "3":
        public_ip_info()

elif choice == "25" or choice == "025":
    print("""
╔══════════════════════════════════════╗
║          DNS RESOLUTION              ║
╠══════════════════════════════════════╣
║  1 • DNS Test                        ║
║  2 • Resolver Test                   ║
║  3 • Resolution Time                 ║
║  4 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("RESOLVE > ").strip()

    if sub_choice == "1":
        dns_test()
    elif sub_choice == "2":
        resolver_test()
    elif sub_choice == "3":
        resolution_time()

elif choice == "26" or choice == "026":
    print("""
╔══════════════════════════════════════╗
║          CONNECTIVITY                ║
╠══════════════════════════════════════╣
║  1 • Internet Test                   ║
║  2 • DNS Test                        ║
║  3 • HTTP Test                       ║
║  4 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("CONNECT > ").strip()

    if sub_choice == "1":
        internet_test()
    elif sub_choice == "2":
        dns_connectivity_test()
    elif sub_choice == "3":
        http_connectivity_test()

elif choice == "27" or choice == "027":
    print("""
╔══════════════════════════════════════╗
║        SYSTEM INFORMATION            ║
╠══════════════════════════════════════╣
║  1 • CPU                             ║
║  2 • RAM                             ║
║  3 • Storage                         ║
║  4 • Operating System                ║
║  5 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("SYSTEM > ").strip()

    if sub_choice == "1":
        cpu_information()
    elif sub_choice == "2":
        ram_information()
    elif sub_choice == "3":
        storage_information()
    elif sub_choice == "4":
        operating_system_information()

elif choice == "28" or choice == "028":
    print("""
╔══════════════════════════════════════╗
║       TEST PAYLOAD GENERATOR         ║
╠══════════════════════════════════════╣
║  1 • Basic Test String               ║
║  2 • Long Input Test                 ║
║  3 • Special Characters              ║
║  4 • Unicode Test                    ║
║  5 • Base64 Test                     ║
║  6 • URL Encoding Test               ║
║  7 • Custom Test Input               ║
║  8 • Back                            ║
╚══════════════════════════════════════╝
""")

    sub_choice = input("PAYLOAD > ").strip()

    if sub_choice == "1":
        basic_test_payload()
    elif sub_choice == "2":
        long_input_test()
    elif sub_choice == "3":
        special_character_test()
    elif sub_choice == "4":
        unicode_test()
    elif sub_choice == "5":
        base64_test()
    elif sub_choice == "6":
        url_encoding_test()
    elif sub_choice == "7":
        custom_test_input()
elif choice == "0" or choice == "00":
                print(couleur("\n👋 Goodbye! ⚡DRAGON TECH⚡ signing off...\n", COULEURS.GREEN + COULEURS.BOLD))
                sys.exit(0)
            else:
                print(couleur("❌ Invalid option. Try again.", COULEURS.RED))

        except KeyboardInterrupt:
            continue
        except Exception as e:
            print(couleur("\n❌ Error: " + str(e), COULEURS.RED))
            input(couleur("Press Enter to continue...", COULEURS.GRAY))

if __name__ == "__main__":
    main()
