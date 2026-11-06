# 🐧 dinstall

<p align="center">
  <b>Inteligentny, terminalowy instalator pakietów i zestawów sieciowych dla systemów Linux.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Linux-blue?style=for-the-badge&logo=linux" alt="Linux">
  <img src="https://img.shields.io/badge/python-3.x-yellow?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
</p>

---

## 🚀 O projekcie

`dinstall` to lekki, napisany w Pythonie menedżer i instalator stworzony z myślą o administratorach sieci oraz osobach pracujących na różnych dystrybucjach Linuksa. Narzędzie automatycznie wykrywa menedżer pakietów w systemie, pozwala na inteligentne instalowanie całych zestawów tematycznych (np. pełny stos DHCP, serwery BIND9, narzędzia diagnostyczne) oraz obsługuje natywne wyszukiwanie w repozytoriach.

## 🛠️ Obsługiwane dystrybucje i menedżery
* **APT** (Debian, Ubuntu, Linux Mint, Kali Linux)
* **DNF / YUM** (Fedora, RHEL, CentOS Stream)
* **Pacman** (Arch Linux, Manjaro, EndeavourOS)
* **Zypper** (openSUSE)

---

## 📥 Instalacja

Sklonuj repozytorium i utwórz globalny skrót w systemie:

```bash
git clone [https://github.com/DevLabStudy/dinstall.git](https://github.com/DevLabStudy/dinstall.git)
cd dinstall
sudo chmod +x dinstall.py
sudo ln -s $(pwd)/dinstall.py /usr/local/bin/dinstall
