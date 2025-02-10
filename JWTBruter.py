import jwt
import concurrent.futures
import logging

# Logging einrichten (besser als viele `print()`-Ausgaben)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def try_decode_jwt(secret):
    """
    Versucht das JWT-Token mit einem bestimmten Secret zu entschlüsseln.
    Gibt das entschlüsselte Token zurück, falls erfolgreich.
    """
    secret = secret.strip()  # Nur einmal entfernen
    try:
        payload = jwt.decode(encoded_token, secret, algorithms=['HS256'])
        logging.info(f"Token erfolgreich mit Passwort entschlüsselt: [{secret}]")
        return secret  # Erfolgreiches Secret zurückgeben
    except jwt.ExpiredSignatureError:
        logging.warning(f"Token abgelaufen mit Passwort: [{secret}]")
    except jwt.InvalidTokenError:
        pass  # Keine Ausgabe für ungültige Versuche

    return None  # Kein Treffer

if __name__ == "__main__":
    print("Brute-Force JWT-Token Cracker")

    # Eingabe des Tokens und der Passwortliste
    encoded_token = input("JWT TOKEN: ")
    passwords_file = input("Pfad zur Passwortliste: ")

    # Passwortliste aus Datei einlesen
    with open(passwords_file, "r") as file:
        passwords = [line.strip() for line in file]  # Direkte Listenkomprimierung

    # Multithreading für schnellere Brute-Force-Angriffe
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(try_decode_jwt, passwords)

    # Überprüfung, ob ein passendes Passwort gefunden wurde
    found_secret = next((r for r in results if r is not None), None)
    if found_secret:
        print(f"✅ JWT entschlüsselt mit Passwort: {found_secret}")
    else:
        print("❌ Kein passendes Passwort gefunden.")
