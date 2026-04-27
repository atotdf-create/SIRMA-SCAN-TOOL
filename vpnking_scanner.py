#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 ██╗   ██╗██████╗ ███╗   ██╗      ██╗  ██╗██╗███╗   ██╗ ██████╗
 ██║   ██║██╔══██╗████╗  ██║      ██║ ██╔╝██║████╗  ██║██╔════╝
 ██║   ██║██████╔╝██╔██╗ ██║█████╗█████╔╝ ██║██╔██╗ ██║██║  ███╗
 ╚██╗ ██╔╝██╔═══╝ ██║╚██╗██║╚════╝██╔═██╗ ██║██║╚██╗██║██║   ██║
  ╚████╔╝ ██║     ██║ ╚████║      ██║  ██╗██║██║ ╚████║╚██████╔╝
   ╚═══╝  ╚═╝     ╚═╝  ╚═══╝      ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝

           👑 VPN-KING SCANNER – BY SIRMA & TDF 👑
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

# ---------- CTRL+C HANDLING ----------
def signal_handler(sig, frame):
    print(couleur("\n\n⚠️  Interruption detected. Returning to menu...", COULEURS.JAUNE))
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
    return f"{code}{text}{COULEURS.RESET}"

# ---------- AUTO INSTALLATION ----------
def is_installed():
    return shutil.which("vpnking") is not None

def install_script():
    print(couleur("\n🔧 FIRST USE – AUTOMATIC INSTALLATION", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("This tool will configure itself to run using the 'vpnking' command under SIRMA framework.", COULEURS.BLUE))

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
        print(couleur(f"✅ Script deployed to {destination} (SIRMA core)", COULEURS.GREEN))
    except Exception as e:
        print(couleur(f"❌ Deployment error: {e}", COULEURS.RED))
        return

    bashrc = os.path.expanduser("~/.bashrc")
    path_line = 'export PATH="$HOME/bin:$PATH"'

    try:
        with open(bashrc, "r") as f:
            content = f.read()

        if path_line not in content:
            with open(bashrc, "a") as f:
                f.write(f"\n# Added by SIRMA VPN-KING SCANNER\n{path_line}\n")
            print(couleur("✅ PATH updated (SIRMA environment)", COULEURS.GREEN))
        else:
            print(couleur("ℹ️ PATH already configured.", COULEURS.BLUE))
    except Exception as e:
        print(couleur(f"⚠️ Cannot modify environment: {e}", COULEURS.YELLOW))

    alias_line = "alias vpnking='python ~/bin/vpnking'"

    try:
        with open(bashrc, "r") as f:
            content = f.read()

        if alias_line not in content:
            with open(bashrc, "a") as f:
                f.write(f"{alias_line}\n")
            print(couleur("✅ Alias added (SIRMA CLI)", COULEURS.GREEN))
    except:
        pass

    print(couleur("\n🎉 SIRMA INSTALLATION COMPLETE!", COULEURS.GREEN + COULEURS.BOLD))
    print(couleur("Restart Termux or run:", COULEURS.BLUE))
    print(couleur("   source ~/.bashrc", COULEURS.YELLOW))
    print(couleur("Then run: vpnking", COULEURS.GREEN))
    input(couleur("\nPress Enter to continue...", COULEURS.GRAY))

# ---------- LOGO ----------
def show_logo():
    logo = f"""
{couleur("╔══════════════════════════════════╗", COULEURS.YELLOW)}
{couleur("║", COULEURS.YELLOW)}  {couleur("👑 VPN-KING SCANNER – SIRMA 👑", COULEURS.GREEN + COULEURS.BOLD)} {couleur("║", COULEURS.YELLOW)}
{couleur("║", COULEURS.YELLOW)}  {couleur("Advanced Recon & Network Intelligence", COULEURS.BLUE)} {couleur("║", COULEURS.YELLOW)}
{couleur("╚══════════════════════════════════╝", COULEURS.YELLOW)}
"""
    print(logo)

# ---------- PASSWORD SYSTEM ----------
PASSWORD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".sirma_pass")

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
            password = getpass.getpass(couleur("🔑 SIRMA Password: ", COULEURS.YELLOW))
        except KeyboardInterrupt:
            print(couleur("\n👋 Exiting SIRMA system...", COULEURS.GREEN))
            sys.exit(0)

        if hash_password(password) == stored_hash:
            print(couleur("✅ SIRMA Access Granted.", COULEURS.GREEN))
            return True
        else:
            attempts -= 1
            print(couleur(f"❌ Incorrect password. {attempts} attempt(s) remaining.", COULEURS.RED))

    print(couleur("🚫 SIRMA Access Denied.", COULEURS.RED))
    sys.exit(1)

def change_password():
    print(couleur("\n🔐 SIRMA Password Change", COULEURS.BLUE))

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
        new = getpass.getpass(couleur("New password: ", COULEURS.YELLOW))
        confirm = getpass.getpass(couleur("Confirm password: ", COULEURS.YELLOW))
    except KeyboardInterrupt:
        print(couleur("\nCancelled.", COULEURS.YELLOW))
        return

    if new != confirm:
        print(couleur("❌ Password mismatch.", COULEURS.RED))
        return

    with open(PASSWORD_FILE, "w") as f:
        f.write(hash_password(new))

    print(couleur("✅ SIRMA password updated successfully.", COULEURS.GREEN))