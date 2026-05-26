import requests 

API_KEY = "XCYINF77NB0FG7RC"
channel_id = "3392340"

while(True):
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={API_KEY}&results=2"
    r = requests.get(url)
    status = requests.status_codes
    heads = requests.headers
    if status == 200:
        print("Donnée reçue")
        print(heads)
    else:
        print("Il y a eu une erreur")
        print(heads)
        print(status)    