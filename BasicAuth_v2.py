import os
import base64
import time
import logging
import requests
from requests.auth import HTTPBasicAuth

# Logging einrichten
logging.basicConfig(
    filename="security_check.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Benutzer & Passwörter aus Umgebungsvariablen (sicherer als Hardcoding)
users = os.getenv("AUTH_USERS", "administrator,admin").split(",")
passwords = os.getenv("AUTH_PASSWORDS", "admin123,admin").split(",")

# Geschützter Bereich (Resource)
protected_resource = "http://localhost/secured"

# Rate Limiting Konfiguration (Schutz gegen Brute-Force)
REQUEST_DELAY = 2  # Sekunden zwischen Anfragen
MAX_ATTEMPTS = 5  # Maximale Versuche pro Benutzer

def test_auth():
    found_pass = False

    for user in users:
        if found_pass:
            break

        attempt_count = 0  # Versuchszähler für Rate-Limiting

        for passwd in passwords:
            if attempt_count >= MAX_ATTEMPTS:
                logging.warning(f"Zu viele Fehlversuche für Benutzer {user}. Wartezeit aktiviert.")
                time.sleep(10)  # Verzögerung nach mehreren Fehlversuchen

            # Sichere Base64-Kodierung (nicht notwendig für `requests`, nur zur Demo)
            credentials = f"{user}:{passwd}".encode("utf-8")
            encoded = base64.b64encode(credentials).decode("utf-8")

            # HTTP-Request mit Fehlerbehandlung
            try:
                response = requests.get(
                    protected_resource, 
                    auth=HTTPBasicAuth(user, passwd),
                    timeout=5  # Timeout-Schutz
                )

                if response.status_code == 200:
                    logging.info(f"Benutzer gefunden: {user} mit Passwort: {passwd}")
                    print(f"User Found! User: {user}, Pass: {passwd}")
                    found_pass = True
                    break
                elif response.status_code == 401:
                    logging.warning(f"Fehlgeschlagene Authentifizierung für {user}")
                else:
                    logging.error(f"Unerwarteter Statuscode {response.status_code} für Benutzer {user}")

            except requests.exceptions.RequestException as e:
                logging.error(f"Fehler bei der Anfrage für {user}: {e}")

            attempt_count += 1
            time.sleep(REQUEST_DELAY)  # Verzögerung zwischen Anfragen

if __name__ == "__main__":
    test_auth()
