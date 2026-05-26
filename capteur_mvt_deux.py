import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

CAPTEUR1 = 17
CAPTEUR2 = 4
LED = 18

distance = 0.20  

GPIO.setup(CAPTEUR1, GPIO.IN)
GPIO.setup(CAPTEUR2, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

print("Initialisation...")
time.sleep(2)
print("Prêt !")

try:
    while True:

        while GPIO.input(CAPTEUR1) == 0:
            pass

        t1 = time.time()
        print("Balle détectée au capteur 1")

        GPIO.output(LED, GPIO.HIGH)

        while GPIO.input(CAPTEUR2) == 0:
            pass

        t2 = time.time()
        print("Balle détectée au capteur 2")

        GPIO.output(LED, GPIO.LOW)

        temps = t2 - t1
        vitesse = distance / temps

        print(f"Temps : {temps:.4f} s")
        print(f"Vitesse : {vitesse:.2f} m/s")

        time.sleep(1)

except KeyboardInterrupt:
    print("Arrêt du programme")

finally:
    GPIO.cleanup()