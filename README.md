# poloniex_python
This is a module to use the Poloniex Exchange API with python.

It is recommended to touch a `key.py` that contains your Poloniex credentials as follows:
```
apikey = 'PASTE_YOUR_API_KEY_HERE'
secret = 'PASTE_YOUR_SECRET_HERE'
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

Any method is called following the format:
```
client.NAME_OF_THE_METHOD()
```

## 2 - Public methods
These methods work without signature, i.e. the Poloniex credentials are NOT mandatory.

### 2.1 - Ticker
Retrieves summary information for each `symbol` listed on the exchange.

Parameter | Mandatory
--------- | ---------
Symbol | No
Field | No
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.
* `Field` can be filled with `id`, `last`, `lowestAsk`, `highestBid`, `percentChange`, `baseVolume`, `quoteVolume`, `isFrozen`, `high24hr`, and `low24hr`.

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

Parameter | Mandatory
--------- | ---------
```
client.rOrderBook()
```
### 2.4 - Market trade history

Parameter | Mandatory
--------- | ---------
```
client.rMarketTradeHistory()
```
### 2.5 - Chart data

Parameter | Mandatory
--------- | ---------
```
client.rChartData()
```
### 2.6 - Currencies

Parameter | Mandatory
--------- | ---------
```
client.rCurrencies()
```
### 2.7 - Loan orders

Parameter | Mandatory
--------- | ---------
```
rLoanOrders()
```
## 3 - Trading methods
Only these methods need signature, i.e. the Poloniex credentials are mandatory.

### 3.1 - Balances

Parameter | Mandatory
--------- | ---------
```
client.rBalances()
```

### 3.2 - Complete balances

Parameter | Mandatory
--------- | ---------
```
client.rCompleteBalances()
```

### 3.3 - Open orders

Parameter | Mandatory
--------- | ---------
```
client.rOpenOrders()
```

### 3.4 - Trade history

Parameter | Mandatory
--------- | ---------
```
client.rTradeHistory()
```

### 3.5 - Limit buy

Parameter | Mandatory
--------- | ---------
```
client.limitBuy()
```

### 3.6 - Limit sell

Parameter | Mandatory
--------- | ---------
```
client.limitSell()
```

### 3.7 - Market buy
The Poloniex REST API has not market orders from default. So this method is a limit order which emulates a market order.

Parameter | Mandatory
--------- | ---------
```
client.marketBuy()
```

### 3.8 - Market sell
The Poloniex REST API has not market orders from default. So this method is a limit order which emulates a market order.

Parameter | Mandatory
--------- | ---------
```
client.marketSell()
```

### 3.9 - Cancel order

Parameter | Mandatory
--------- | ---------
```
client.cancelOrder()
```

### 3.10 - Cancel all orders

Parameter | Mandatory
--------- | ---------
```
client.cancelAllOrders()
```

### 3.11 - Withdraw

Parameter | Mandatory
--------- | ---------
```
client.withdraw()
```

## 4 - Websocket methods
Coming soon.
