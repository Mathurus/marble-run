import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BCM)

CAPTEUR1 = 17
CAPTEUR2 = 4
LED = 18

DISTANCE = 0.20
TIMEOUT = 5.0
VITESSE_MAX = 100.0
TEMPS_MIN = DISTANCE / VITESSE_MAX   
THINGSPEAK_DELAY = 15

API_KEY = "O8HE149XGWLH8WDD"

GPIO.setup(CAPTEUR1, GPIO.IN)
GPIO.setup(CAPTEUR2, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

dernier_envoi = 0

def envoyer_vitesse(vitesse):
    try:
        url = f"https://api.thingspeak.com/update?api_key={API_KEY}&field1={vitesse:.2f}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200 and r.text != "0":
            print(f"Envoi réussi → {vitesse:.2f} m/s (entry ID: {r.text})")
        elif r.text == "0":
            print("Envoi refusé par ThingSpeak (rate limit 15s)")
        else:
            print(f"Échec de l'envoi (code {r.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau : {e}")

print("Initialisation...")
time.sleep(2)
print("Prêt !")

try:
    while True:

        while GPIO.input(CAPTEUR1) == 1:
            pass

        while GPIO.input(CAPTEUR1) == 0:
            pass
        t1 = time.time()
        print("Balle détectée au capteur 1")
        GPIO.output(LED, GPIO.HIGH)

        time.sleep(0.005)

        t_debut = time.time()
        detecte = False
        while time.time() - t_debut < TIMEOUT:
            if GPIO.input(CAPTEUR2) == 1:
                t2 = time.time()
                detecte = True
                break

        GPIO.output(LED, GPIO.LOW)

        if not detecte:
            print("Timeout : balle non détectée au capteur 2\n")
            time.sleep(1)
            continue

        print("Balle détectée au capteur 2")

        temps = t2 - t1
        vitesse = DISTANCE / temps

        print(f"Temps   : {temps:.4f} s")
        print(f"Vitesse : {vitesse:.2f} m/s")

        if temps < TEMPS_MIN:
            print(f"Mesure ignorée (crosstalk détecté, temps trop court : {temps:.4f}s)\n")
        else:
            now = time.time()
            if now - dernier_envoi >= THINGSPEAK_DELAY:
                envoyer_vitesse(vitesse)
                dernier_envoi = now
            else:
                attente = THINGSPEAK_DELAY - (now - dernier_envoi)
                print(f"Rate limit : prochain envoi dans {attente:.0f}s")
            print()

        time.sleep(1)

except KeyboardInterrupt:
    print("Arrêt du programme")

finally:
    GPIO.cleanup()