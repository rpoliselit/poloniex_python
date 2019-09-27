# poloniex_python
Module to use the Poloniex Exchange API with python.

It is recommended to touch a `key.py` that contains your poloniex credentials as follows:
```
apikey = 'paste_your_api_key_here'
secret = 'paste_your_secret_here'
```

Importing the Poloniex class in your code:
```
from poloniex_api import poloniex
import key
```

## 1 - Client
First of all make the following client assignment:
```
client = poloniex(key.apikey, key.secret)
```
Any method is called as:
```
client.SOMEMETHOD()
```

## 2 - Public methods
These methods work without signature, i.e. it is not mandatory the Poloniex credentials in order to use them.

### 2.1 - Ticker
Retrieves summary information for each `symbol` listed on the exchange. Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, BTC is used as currency to buy a given asset, LTC.

Parameter | Mandatory
--------- | ---------
Symbol | No
Field | No

`Field` can be filled with `id`, `last`, `lowestAsk`, `highestBid`, `percentChange`, `baseVolume`, `quoteVolume`, `isFrozen`, `high24hr`, and `low24hr`.

Example:
```
client.rTicker('BTC_LTC', 'last')
```

### 2.2 - 24h volume
Returns the 24-hour volume for all markets as well as totals for primary currencies.

Parameter | Mandatory
--------- | ---------
Symbol | No
Currency/Asset | No

Example:
```
client.r24hVolume('BTC_LTC', 'LTC')
```
### 2.3 - Order book
```
client.rOrderBook()
```
### 2.4 - Market trade history
```
client.rMarketTradeHistory()
```
### 2.5 - Chart data
```
client.rChartData()
```
### 2.6 - Currencies
```
client.rCurrencies()
```
### 2.7 - Loan orders
```
rLoanOrders()
```
## 3 - Trade methods
Only theses methods needs signature.

## 4 - Websocket methods
Coming soon.
