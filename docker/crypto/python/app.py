import time
import requests
import paho.mqtt.client as mqtt


BROKER = "mosquitto"
PORT = 1883

INTERVALO = 60

URL_API = "https://api.coingecko.com/api/v3/simple/price"

PARAMETROS = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "eur",
    "include_market_cap": "true",
    "include_24hr_vol": "true"
}


def obtener_datos():

    respuesta = requests.get(
        URL_API,
        params=PARAMETROS,
        timeout=10
    )

    respuesta.raise_for_status()

    return respuesta.json()


def publicar_datos(cliente, datos):

    for moneda, valores in datos.items():

        precio = valores.get("eur")
        market_cap = valores.get("eur_market_cap")
        volumen = valores.get("eur_24h_vol")

        cliente.publish(
            f"crypto/{moneda}/price",
            str(precio)
        )

        cliente.publish(
            f"crypto/{moneda}/market_cap",
            str(market_cap)
        )

        cliente.publish(
            f"crypto/{moneda}/volume",
            str(volumen)
        )

        print(
            f"{moneda}: "
            f"precio={precio} €, "
            f"market_cap={market_cap}, "
            f"volumen={volumen}"
        )


def main():

    cliente = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="crypto-api"
    )

    print("Conectando con Mosquitto...")

    cliente.connect(BROKER, PORT, 60)

    cliente.loop_start()

    print("Conectado correctamente al broker MQTT")

    while True:

        try:

            print("Consultando CoinGecko...")

            datos = obtener_datos()

            publicar_datos(cliente, datos)

            print("Datos publicados correctamente")

        except Exception as error:

            print(f"ERROR: {error}")

        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
