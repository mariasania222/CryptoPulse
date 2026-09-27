import requests
import paho.mqtt.client as mqtt
import time

MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883

TOPIC_PRICE = "crypto/bitcoin/price"
TOPIC_MARKET_CAP = "crypto/bitcoin/market_cap"
TOPIC_VOLUME = "crypto/bitcoin/volume"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        price = data["bitcoin"]["usd"]
        market_cap = data["bitcoin"]["usd_market_cap"]
        volume = data["bitcoin"]["usd_24h_vol"]

        client.publish(TOPIC_PRICE, price)
        client.publish(TOPIC_MARKET_CAP, market_cap)
        client.publish(TOPIC_VOLUME, volume)

        print(f"Bitcoin price: {price} USD")
        print(f"Bitcoin market cap: {market_cap} USD")
        print(f"Bitcoin volume 24h: {volume} USD")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(60)
