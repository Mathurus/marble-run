import requests

valeur = 20

API_KEY = "O8HE149XGWLH8WDD"

while(True):
    url = f"https://api.thingspeak.com/update?api_key={API_KEY}&field1={valeur}"
    r = requests.get(url)
    status = r.status_code
    head = r.headers
    if status == 200:
        print("Envoie réussi :) ")
        print(r, head)
        print(r.text)
    else:
        print("echec de l'envoie ")
