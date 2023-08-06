import requests
import json
import argparse


sources = [
    "bitstamp",
    "binance",
    "coingecko",
]

def get_crypto_price(source = "bitstamp", crypto = "btc", pair = "usdt"):

    if source in sources:
        URL = None

        if source == "bitstamp":
            URL = f"https://www.bitstamp.net/api/v2/ticker/{crypto+pair}"
        elif source == "binance":
            URL = f"https://api.binance.com/api/v3/ticker/price?symbol={crypto+pair}"
        elif source == "coingecko":
            URL = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={pair}"


        if not URL is None:

            try:
                r = requests.get(URL)
                if source == "bitstamp":
                    priceFloat = float(json.loads(r.text)["last"])
                elif source == "binance":
                    priceFloat = float(json.loads(r.text)["price"])
                elif source == "coingecko":
                    priceFloat = float(json.loads(r.text)[crypto][pair])
                return priceFloat

            except requests.ConnectionError:
                print("Error querying API")
            except json.decoder.JSONDecodeError:
                print("Error querying pair")

    else:
        print("Availale sources: ")
        for each_source in sources:
            print(each_source)
        raise "Source is unavailable"

def arguments():
    source = "bitstamp"
    crypto = "btc"
    pair = "usdt"

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, help='Source')
    parser.add_argument('-c', '--crypto', type=str, help='Crypto')
    parser.add_argument('-p', '--pair', type=str, help='Pair')

    args = parser.parse_args()

    if not args.source is None:
        source = args.source
    if not args.crypto is None:
        crypto = args.crypto        
    if not args.pair is None:
        pair = args.pair

    return get_crypto_price(source=source, crypto=crypto, pair=pair)
