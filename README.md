# poloniex_python
Here we have a non-official module to use the Poloniex Exchange API with python 3. Any questions about the API check out the official documentation at https://docs.poloniex.com/#introduction. Our code uses [aiohttp](https://aiohttp.readthedocs.io/en/stable/) and [asyncio](https://docs.python.org/3/library/asyncio.html) libraries in order to interact with the exchange server.

Poloniex provides both HTTP and websocket APIs for interacting with the exchange. Both allow read access to public market data and private read access to your account. Private write access to your account is available via the private HTTP API.

The public HTTP endpoint is accessed via `GET` requests while the private endpoint is accessed via `HMAC-SHA512` signed `POST` requests using API keys. Both types of HTTP endpoints return results in `JSON` format.

The websocket API allows push notifications about the public order books, lend books and your private account. Similarly to the HTTP API, it requires `HMAC-SHA512` signed requests using API keys for requests related to your private account.

## Get starting

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

### Client
The 'poloniex' class is the object that connects you to Poloniex's server as a client. Its initial parameters are your credentials in exchange: API key and secret.

First of all make the following client assignment:
```
client = poloniex(key.apikey, key.secret)
```

Any method is called following the format:
```
client.NAME_OF_THE_METHOD()
```

From now on we have all the methods described, exemplified, and ordered as the summary:
- [Public HTTP methods](#public-http-methods)
 - [Ticker](#ticker)
 - [24h volume](#24h-volume)
 - [Order book](#order-book)
 - [Market trade history](#market-trade-history)
 - [Chart date](#chart-data)
 - [Currencies](#currencies)
 - [Loan orders](#loan-orders)
- [Private HTTP methods](#private-http-methods)
 - [Balances](#balances)
 - [Complete balances](#complete-balances)
 - [Open orders](#open-orders)
 - [Trade history](#trade-history)
 - [Limit buy](#limit-buy)
 - [Limit sell](#limit-sell)
 - [Market buy](#market-buy)
 - [Market sell](#market-sell)
 - [Cancel order](#cancel-order)
 - [Cancel all orders](#cancel-all-orders)
 - [Withdraw](#withdraw)
 - [Deposit address](#deposit-address)
 - [Generate new addresses](#generate-new-addresses)
 - [Deposits and withdraws history](#deposits-and-withdraws-history)
- [Websocket methods](#websocket-methods)

## Public HTTP methods
These methods work without signature, i.e. the Poloniex credentials are NOT mandatory.
* The base endpoint is: https://poloniex.com/public
* Endpoint returns JSON object.
* All methods can return either JSON object, or array, or float.

### Ticker
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

### 24h volume
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

### Order book
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

### Market trade history
Returns the past 200 trades for a given market.

Parameter | Mandatory
--------- | ---------
symbol | Yes
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.

```
client.rMarketTradeHistory('BTC_LTC')
```

### Chart data
Returns candlestick chart data. `start` and `end` are given as `YEAR-MONTH-DAY HOUR:MINUTES:SECONDS`.

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

### Currencies
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

### Loan orders
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

## Private HTTP methods
These methods need signature, i.e. the Poloniex credentials are mandatory.

### Balances
Returns all of your balances available for trade after having deducted all open orders.

Parameter | Mandatory
--------- | ---------
currency | No
* `currency` refers to abbreviation of a given asset name. For instance `BTC` is the abbreviation of Bitcoin.

```
client.rBalances('BTC')
```

### Complete balances
Returns all of your balances, including available balance, balance on orders, and the estimated BTC value of your balance.

Parameter | Mandatory
--------- | ---------
currency | No
field | No
* `currency` refers to abbreviation of a given asset name. For instance `BTC` is the abbreviation of Bitcoin.
* `field` can be filled with `available`,`onOrders`, and `btcValue`.

```
client.rCompleteBalances('BTC', 'available')
```

### Open orders
Returns your open orders for a given market.

Parameter | Mandatory
--------- | ---------
symbol | Yes
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`. _Note_: `symbol` is mandatory following the API, however here the default value is `all`.

```
client.rOpenOrders('BTC_LTC')
```

### Trade history
Returns your trade history for a given market. `start` and `end` are given as `YEAR-MONTH-DAY HOUR:MINUTES:SECONDS`.

Parameter | Mandatory
--------- | ---------
symbol | Yes
start | No
end | No
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`. _Note_: `symbol` is mandatory following the API, however here the default value is `all`.
* `start` of time window.
* `end` of time window.
* The range between `start` and `end` is limited to one day.

```
client.rTradeHistory('BTC_LTC')
```

### Limit buy

Parameter | Mandatory
--------- | ---------
```
client.limitBuy()
```

### Limit sell

Parameter | Mandatory
--------- | ---------
```
client.limitSell()
```

### Market buy
The Poloniex REST API has not market orders from default. So this method is a limit order which emulates a market order.

Parameter | Mandatory
--------- | ---------
```
client.marketBuy()
```

### Market sell
The Poloniex REST API has not market orders from default. So this method is a limit order which emulates a market order.

Parameter | Mandatory
--------- | ---------
```
client.marketSell()
```

### Cancel order

Parameter | Mandatory
--------- | ---------
```
client.cancelOrder()
```

### Cancel all orders

Parameter | Mandatory
--------- | ---------
```
client.cancelAllOrders()
```

### Withdraw

Parameter | Mandatory
--------- | ---------
```
client.withdraw()
```

### Deposit address
Coming soon.
### Generate new addresses
Coming soon.
### Deposits and withdraws history
Coming soon.

## Websocket methods
Coming soon.
