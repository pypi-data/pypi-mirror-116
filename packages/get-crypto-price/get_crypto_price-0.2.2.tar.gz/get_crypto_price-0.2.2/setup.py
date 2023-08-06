from setuptools import setup


setup(name='get_crypto_price',
version='0.2.2',
description="""A library to getting crypto price.""",
long_description="""
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
""",
long_description_content_type='text/markdown',
url='https://github.com/onuratakan/get_crypto_price',
author='Onur Atakan ULUSOY',
author_email='atadogan06@gmail.com',
license='MIT',
packages=["get_crypto_price"],
package_dir={'':'src'},
install_requires=[
    "requests==2.25.1"
],
entry_points = {
    'console_scripts': ['get_crypto_price=get_crypto_price.get_crypto_price:arguments'],
},
python_requires=">= 3",
zip_safe=False)