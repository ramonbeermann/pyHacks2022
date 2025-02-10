#!/usr/bin/env python3
import platform
import subprocess
import concurrent.futures
import logging

# Logging für bessere Übersichtlichkeit
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Erkennen, welches Betriebssystem verwendet wird (Windows oder Linux/macOS)
system_os = platform.system()
ping_cmd = ["ping", "-c", "1"] if system_os != "Windows" else ["ping", "-n", "1"]

# Speichert erfolgreiche IPs in eine Datei
OUTPUT_FILE = "ips.txt"

def ping_ip(ip):
    """
    Ping eine IP-Adresse und gibt zurück, ob sie erreichbar ist.
    """
    try:
        result = subprocess.run(ping_cmd + [ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "bytes from" in result.stdout or "TTL=" in result.stdout:  # "TTL=" für Windows-Erkennung
            logging.info(f"✔ IP {ip} ist erreichbar!")
            with open(OUTPUT_FILE, "a") as file:
                file.write(ip + "\n")
            return ip
    except Exception as e:
        logging.error(f"Fehler beim Pingen von {ip}: {e}")
    return None

def scan_network(base_ip, start=1, end=40):
    """
    Scannt einen IP-Bereich parallel mit Threads.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        ip_range = [f"{base_ip}.{i}" for i in range(start, end + 1)]
        results = executor.map(ping_ip, ip_range)
    
    # Erfolgreiche IPs ausgeben
    active_ips = [ip for ip in results if ip]
    if active_ips:
        logging.info("🔍 Erreichbare IPs gespeichert in ips.txt")
    else:
        logging.warning("❌ Keine erreichbaren IPs gefunden.")

if __name__ == "__main__":
    print("🔎 Effizienter Ping-Scanner")
    base_network = input("Gib das Subnetz an (z. B. 192.168.1): ").strip()
    start_ip = int(input("Start-IP (Standard: 1): ") or 1)
    end_ip = int(input("End-IP (Standard: 40): ") or 40)

    scan_network(base_network, start_ip, end_ip)
