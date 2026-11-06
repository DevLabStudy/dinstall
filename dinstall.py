#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

# Definicja inteligentnych grup pakietów z uwzględnieniem nowoczesnych standardów i dystrybucji
SMART_BUNDLES = {
    "dhcp": {
        "name": "Nowoczesny Serwer DHCP (Kea DHCP)",
        "description": "Instaluje nowoczesny serwer Kea DHCPv4 oraz narzędzia sieciowe",
        "packages": {
            "apt": ["kea-dhcp4-server", "net-tools", "dhcping"],
            "dnf": ["kea-dhcp4", "net-tools", "dhcping"],
            "pacman": ["kea", "net-tools", "dhcping"]
        }
    },
    "dns-bind": {
        "name": "Serwer DNS (BIND9)",
        "description": "Pełna instalacja i konfiguracja serwera nazw BIND",
        "packages": {
            "apt": ["bind9", "bind9utils", "dnsutils"],
            "dnf": ["bind", "bind-utils"],
            "pacman": ["bind", "dnsutils"]
        }
    },
    "network-tools": {
        "name": "Zaawansowany Toolkit Sieciowy",
        "description": "Nmap, tcpdump, traceroute, iperf3, curl, netcat",
        "packages": {
            "apt": ["nmap", "tcpdump", "traceroute", "iperf3", "curl", "netcat-traditional"],
            "dnf": ["nmap", "tcpdump", "traceroute", "iperf3", "curl", "nmap-ncat"],
            "pacman": ["nmap", "tcpdump", "traceroute", "iperf3", "curl", "gnu-netcat"]
        }
    },
    "web-stack": {
        "name": "Stos Webowy (Nginx + PHP + MariaDB)",
        "description": "Podstawowe środowisko pod serwery www i panele",
        "packages": {
            "apt": ["nginx", "mariadb-server", "php-fpm", "php-mysql"],
            "dnf": ["nginx", "mariadb-server", "php-fpm", "php-mysqlnd"],
            "pacman": ["nginx", "mariadb", "php", "php-fpm"]
        }
    }
}

def check_root():
    if os.geteuid() != 0:
        print("\033[91m[!] Błąd: Uruchom program z uprawnieniami root (sudo python3 dinstall.py).\033[0m")
        sys.exit(1)

def detect_manager():
    if os.path.exists("/usr/bin/apt") or os.path.exists("/bin/apt"):
        return "apt"
    elif os.path.exists("/usr/bin/dnf") or os.path.exists("/bin/dnf"):
        return "dnf"
    elif os.path.exists("/usr/bin/pacman"):
        return "pacman"
    elif os.path.exists("/usr/bin/zypper"):
        return "zypper"
    return "unknown"

def get_os_info():
    try:
        with open("/etc/os-release") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=")[1].strip().strip('"')
    except:
        return platform.system()

def install_packages(package_list):
    manager = detect_manager()
    if not package_list:
        print("[!] Brak pakietów do instalacji.")
        return

    if manager == "apt":
        subprocess.run(["apt", "update"])
        cmd = ["apt", "install", "-y"] + package_list
    elif manager == "dnf":
        cmd = ["dnf", "install", "-y"] + package_list
    elif manager == "pacman":
        cmd = ["pacman", "-Syu", "--noconfirm"] + package_list
    elif manager == "zypper":
        cmd = ["zypper", "install", "-y"] + package_list
    else:
        print("[!] Nieobsługiwany menedżer pakietów.")
        return

    print(f"\n[*] Uruchamiam instalację poleceniem: {' '.join(cmd)}")
    subprocess.run(cmd)

def search_packages(query):
    manager = detect_manager()
    print(f"\n[*] Wyszukiwanie pakietów dla zapytania: '{query}'...")
    
    if manager == "apt":
        subprocess.run(["apt-cache", "search", query])
    elif manager == "dnf":
        subprocess.run(["dnf", "search", query])
    elif manager == "pacman":
        subprocess.run(["pacman", "-Ss", query])
    elif manager == "zypper":
        subprocess.run(["zypper", "search", query])
    else:
        print("[!] Wyszukiwanie niedostępne dla tego systemu.")

def main_menu():
    check_root()
    manager = detect_manager()
    os_name = get_os_info()

    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("==================================================")
        print("          DINSTALL - Linux Package Hub            ")
        print("==================================================")
        print(f" System: {os_name}")
        print(f" Wykryty menedżer pakietów: {manager.upper()}")
        print("==================================================")
        print(" [1] Wybierz inteligentny pakiet / zestaw (Bundle)")
        print(" [2] Wyszukaj i zainstaluj pakiet z repozytorium")
        print(" [3] Wyjdź")
        print("==================================================")
        
        choice = input("Wybierz opcję (1-3): ").strip()

        if choice == "1":
            print("\n--- DOSTĘPNE ZESTAWY INTELIGENTNE ---")
            keys = list(SMART_BUNDLES.keys())
            for idx, key in enumerate(keys, 1):
                bundle = SMART_BUNDLES[key]
                print(f" [{idx}] {bundle['name']} - {bundle['description']}")
            print(f" [{len(keys)+1}] Powrót do menu głównego")
            
            b_choice = input("\nWybierz zestaw: ").strip()
            if b_choice.isdigit():
                b_idx = int(b_choice) - 1
                if 0 <= b_idx < len(keys):
                    selected_key = keys[b_idx]
                    bundle_data = SMART_BUNDLES[selected_key]
                    pkgs = bundle_data["packages"].get(manager, [])
                    print(f"\n[+] Wybrano zestaw: {bundle_data['name']}")
                    print(f"[+] Pakiety do instalacji: {', '.join(pkgs)}")
                    confirm = input("Czy chcesz kontynuować instalację? (t/n): ").strip().lower()
                    if confirm == 't':
                        install_packages(pkgs)
                        input("\nNaciśnij Enter, aby kontynuować...")
        
        elif choice == "2":
            query = input("\nPodaj nazwę pakietu lub frazę do wyszukania: ").strip()
            if query:
                search_packages(query)
                print("\n")
                pkg_to_install = input("Wpisz nazwę pakietu do instalacji (lub zostaw puste, aby wrócić): ").strip()
                if pkg_to_install:
                    install_packages([pkg_to_install])
            input("\nNaciśnij Enter, aby kontynuować...")

        elif choice == "3":
            print("\nDo zobaczenia!")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()