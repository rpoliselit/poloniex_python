# poloniex_python
This is a module to use the Poloniex Exchange API with python. Any questions about the API check out the official documentation at https://docs.poloniex.com/#introduction.

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
symbol | No
field | No
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.
* `field` can be filled with `id`, `last`, `lowestAsk`, `highestBid`, `percentChange`, `baseVolume`, `quoteVolume`, `isFrozen`, `high24hr`, and `low24hr`.

Example:
```
client.rTicker('BTC_LTC', 'last')
```

### 2.2 - 24h volume
Returns the 24-hour volume for all markets as well as totals for primary currencies.

Parameter | Mandatory
--------- | ---------
symbol | No
currency | No
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.
* `currency` refers to currency or asset from a given `symbol`.

Example:
```
client.r24hVolume('BTC_LTC', 'LTC')
```

### 2.3 - Order book
Returns the order book for a given market, as well as a sequence number used by websockets for synchronization of book updates and an indicator specifying whether the market is frozen.

Parameter | Mandatory
--------- | ---------
symbol | Yes
depth | Yes
field | No
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.
* `depth` means the amount of `asks` and `bids` in response. Its maximum value is 100. _Note_: Consider using the Websocket API over HTTP if you are looking for fresh and full order book depth.
* `field` can be filled with `asks`, `bids`, `isFrozen`, and `seq`.
* `symbol` and `depth` are mandatory following the API, however here the default value for both are, respectively, `all` and `50`.

```
client.rOrderBook('BTC_LTC', 4, 'asks')
```

### 2.4 - Market trade history
Returns the past 200 trades for a given market.

Parameter | Mandatory
--------- | ---------
symbol | Yes
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.

```
client.rMarketTradeHistory('BTC_LTC')
```

### 2.5 - Chart data
Returns candlestick chart data.
`start` and `end` are given as `YEAR-MONTH-DAY HOUR:MINUTES:SECONDS`.

Parameter | Mandatory
--------- | ---------
symbol | Yes
start | Yes
period | Yes
end | No
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.
* `start` of the window.
* `end` of the window.
* `period` refers to candlestick period in seconds. Valid values are 300, 900, 1800, 7200, 14400, and 86400.

Example:
```
client.rChartData('BTC_LTC', '2019-08-18 18:45:00', 300)
```

### 2.6 - Currencies
Returns information about currencies.

Parameter | Mandatory
--------- | ---------
currency | No
field | No
* `currency` refers to abbreviation of a given asset name. For instance `BTC` is the abbreviation of Bitcoin.
* `field` can be filled with `id`, `name`, `txFee`, `minConf`, `depositAddress`, `disabled`, `delisted`, `frozen`, and `isGeofenced`

Example:
```
client.rCurrencies('BTC', 'txFee')
```

### 2.7 - Loan orders
Returns the list of loan offers and demands for a given currency.

Parameter | Mandatory
--------- | ---------
currency | Yes
field | No
* `currency` refers to abbreviation of a given asset name. For instance `BTC` is the abbreviation of Bitcoin.
* `field` can be filled with `offers` and `demands`

Example:
```
client.rLoanOrders('BTC','offers')
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
