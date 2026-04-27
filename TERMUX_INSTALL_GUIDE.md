# VPN-KING Scanner – Termux Installation Guide

## Quick Install (Copy & Paste These Commands)

### Step 1: Update Termux
```
pkg update -y && pkg upgrade -y
```

### Step 2: Install Python
```
pkg install python -y
```

### Step 3: Install Git (optional, for cloning from GitHub)
```
pkg install git -y
```

### Step 4: Install Termux API (for wakelock)
```
pkg install termux-api -y
```

### Step 5: Download the script from your GitHub repo
```
git clone https://github.com/atotdf-create/SIRMA-SCAN-TOOL.git
cd SIRMA-SCAN-TOOL
```

### Step 6: Enable Wakelock (keeps phone awake 24/7)
```
termux-wake-lock
```

### Step 7: Run the tool
```
python vpnking_scanner.py
```

---

## One-Liner Install (All in One Command)
```
pkg update -y && pkg upgrade -y && pkg install python git termux-api -y && termux-wake-lock && git clone https://github.com/atotdf-create/SIRMA-SCAN-TOOL.git && cd SIRMA-SCAN-TOOL && python vpnking_scanner.py
```

---

## Auto-Start on Termux Boot

### Option 1: Add to .bashrc
```
echo 'termux-wake-lock' >> ~/.bashrc
```

### Option 2: Install Termux:Boot app
1. Install "Termux:Boot" from F-Droid
2. Create boot script:
```
mkdir -p ~/.termux/boot
echo '#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd ~/SIRMA-SCAN-TOOL
python vpnking_scanner.py' > ~/.termux/boot/start-vpnking.sh
chmod +x ~/.termux/boot/start-vpnking.sh
```

---

## Default Password
The default password is: **tdftech**
You can change it from the menu (Option 12).

## After First Run
The tool will auto-install itself as the `vpnking` command.
After installation, just type `vpnking` to run it from anywhere.
