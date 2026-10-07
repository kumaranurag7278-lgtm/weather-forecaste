import os
import requests

API_KEY = os.environ["OWM_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MY_LATITUDE = 0.0      # put your city's latitude
MY_LONGITUDE = 0.0     # put your city's longitude

parameters = {
    "lat": MY_LATITUDE,
    "lon": MY_LONGITUDE,
    "appid": API_KEY,
    "cnt": 4,          # next 12 hours (4 slots of 3 hours)
}

response = requests.get(
    url="https://api.openweathermap.org/data/2.5/forecast",
    params=parameters,
)
response.raise_for_status()
data = response.json()

will_rain = False
for slot in data["list"]:
    if int(slot["weather"][0]["id"]) < 600:
        will_rain = True

if will_rain:
    body = "It's going to rain today. Remember to bring an umbrella. ☔"
else:
    body = "No rain expected today. 🌤️"

r = requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": body},
)
r.raise_for_status()
print("Sent:", body)