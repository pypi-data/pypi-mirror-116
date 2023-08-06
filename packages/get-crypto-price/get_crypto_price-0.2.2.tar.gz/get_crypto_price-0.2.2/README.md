# Get Crypto Price
A library to getting crypto price.
# Install
```
pip3 install get-crypto-price
```
# Using
## In another script
```python
from get_crypto_price import get_crypto_price
# get_crypto_price(source = "bitstamp", crypto="btc", pair = "usdt")
print(get_crypto_price())
```
## In command line
```console
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Source
  -c CRYPTO, --crypto CRYPTO
                        Crypto
  -p PAIR, --pair PAIR  Pair
```
```console
get_crypto_price
```