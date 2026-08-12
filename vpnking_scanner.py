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
    logo = "\n" + couleur("╔═══════════════════════════════════════════╗", COULEURS.YELLOW) + "\n" + \
           couleur("║", COULEURS.YELLOW) + "  " + couleur("⚡ VPN-KING SCANNER – DRAGON TECH ⚡", COULEURS.GREEN + COULEURS.BOLD) + "  " + couleur("║", COULEURS.YELLOW) + "\n" + \
           couleur("║", COULEURS.YELLOW) + "  " + couleur("  Advanced Recon & Network Intelligence  ", COULEURS.BLUE) + " " + couleur("║", COULEURS.YELLOW) + "\n" + \
           couleur("║", COULEURS.YELLOW) + "  " + couleur("         Version 2.0 – ⚡DRAGON TECH⚡         ", COULEURS.GRAY) + couleur("║", COULEURS.YELLOW) + "\n" + \
           couleur("╚═══════════════════════════════════════════╝", COULEURS.YELLOW)
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

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    stop = start_loading("Analyzing website headers and content...")
    headers, html = http_get_headers(url)
    stop.set()

    if not headers:
        print(couleur("❌ Could not connect or retrieve data from " + url, COULEURS.RED))
        input(couleur("\nPress Enter to continue...", COULEURS.GRAY))
        return

    print(couleur("\n✅ Analysis for: " + url + "\n", COULEURS.GREEN))
    
    server = headers.get("Server", "Unknown")
    powered_by = headers.get("X-Powered-By", "Unknown")
    content_type = headers.get("Content-Type", "Unknown")
    
    print(couleur("  HTTP Headers:", COULEURS.BOLD + COULEURS.WHITE))
    print(couleur("    → Server: " + server, COULEURS.CYAN))
    print(couleur("    → X-Powered-By: " + powered_by, COULEURS.CYAN))
    print(couleur("    → Content-Type: " + content_type, COULEURS.CYAN))
    
    if html:
        print(couleur("\n  Frameworks / Technologies (Signature Check):", COULEURS.BOLD + COULEURS.WHITE))
        html_lower = html.lower()
        techs = []
        if "wordpress" in html_lower or "wp-content" in html_lower:
            techs.append("WordPress")
        if "react" in html_lower or "__react" in html_lower:
            techs.append("React")
        if "vue" in html_lower or "__vue" in html_lower:
            techs.append("Vue.js")
        if "bootstrap" in html_lower:
            techs.append("Bootstrap")
        if "jquery" in html_lower:
            techs.append("jQuery")
        if "shopify" in html_lower:
            techs.append("Shopify")
        if "cloudflare" in html_lower or headers.get("CF-Ray"):
            techs.append("Cloudflare")
        
        if techs:
            for t in techs:
                print(couleur("    → Detected: " + t, COULEURS.GREEN))
        else:
            print(couleur("    → No common signatures detected in HTML body.", COULEURS.GRAY))

    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ========== MAIN MENU ==========
def main():
    if not is_installed():
        install_script()
    
    show_logo()
    verify_password()

    while True:
        print(couleur("\n=============================================", COULEURS.YELLOW))
        print(couleur("          ⚡ VPN-KING MAIN MENU ⚡           ", COULEURS.GREEN + COULEURS.BOLD))
        print(couleur("=============================================", COULEURS.YELLOW))
        print(couleur("  [1] Subdomain Scanner", COULEURS.CYAN))
        print(couleur("  [2] Port Scanner", COULEURS.CYAN))
        print(couleur("  [3] IP Lookup / WHOIS", COULEURS.CYAN))
        print(couleur("  [4] DNS Lookup", COULEURS.CYAN))
        print(couleur("  [5] Reverse IP Lookup", COULEURS.CYAN))
        print(couleur("  [6] Website Technology Detection", COULEURS.CYAN))
        print(couleur("  [7] Change Password", COULEURS.CYAN))
        print(couleur("  [0] Exit", COULEURS.RED))
        print(couleur("=============================================", COULEURS.YELLOW))

        try:
            choice = input(couleur("Select option: ", COULEURS.YELLOW)).strip()
        except KeyboardInterrupt:
            print(couleur("\n👋 Exiting...", COULEURS.GREEN))
            sys.exit(0)

        if choice == "1":
            subdomain_scanner()
        elif choice == "2":
            port_scanner()
        elif choice == "3":
            ip_lookup()
        elif choice == "4":
            dns_lookup()
        elif choice == "5":
            reverse_ip_lookup()
        elif choice == "6":
            tech_detection()
        elif choice == "7":
            change_password()
        elif choice == "0":
            print(couleur("👋 Thank you for using VPN-KING SCANNER. Goodbye!", COULEURS.GREEN))
            sys.exit(0)
        else:
            print(couleur("❌ Invalid choice. Please select a valid option.", COULEURS.RED))
            time.sleep(1)

if __name__ == "__main__":
    main()
