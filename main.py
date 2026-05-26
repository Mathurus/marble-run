import requests 
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PIR = 17
LED = 18
x = 0

GPIO.setup(PIR, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

print("Capteur en cours de démarrage...")
time.sleep(2)

print("Prêt !")

try:
    while True:

        mouvement = GPIO.input(PIR)

        if mouvement:
            x += 1
            print(x, " : ", "Mouvement détecté !")
            GPIO.output(LED, GPIO.HIGH)

        else:
            GPIO.output(LED, GPIO.LOW)

        time.sleep(0.2)

except KeyboardInterrupt:
    print("Arrêt du programme")

finally:
    GPIO.cleanup()