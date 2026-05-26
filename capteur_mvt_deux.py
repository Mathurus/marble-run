import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

CAPTEUR1 = 17
CAPTEUR2 = 4
LED = 18

DISTANCE = 0.20
TIMEOUT = 5.0
VITESSE_MAX = 100.0

GPIO.setup(CAPTEUR1, GPIO.IN)
GPIO.setup(CAPTEUR2, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

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

        if vitesse > VITESSE_MAX:
            print(f"Mesure ignorée (vitesse irréaliste : {vitesse:.1f} m/s)\n")
        else:
            print(f"Temps   : {temps:.4f} s")
            print(f"Vitesse : {vitesse:.2f} m/s\n")

        time.sleep(1)

except KeyboardInterrupt:
    print("Arrêt du programme")

finally:
    GPIO.cleanup()