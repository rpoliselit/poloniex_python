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
The 'poloniex' class is the object that connects you to Poloniex's server as a client. Its initial parameters are your credentials in exchange: `apikey` and `secret`.

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
* The base endpoint is: https://poloniex.com/tradingApi
* Endpoint returns JSON object.
* All methods can return either JSON object, or array.

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
Places a limit buy order in a given market. If successful, the method will return the order number.

Parameter | Mandatory
--------- | ---------
symbol | Yes
rate | Yes
amount | Yes
fok | No
ioc | No
po | No
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.
* The `rate` to purchase the `ASSET` in `CURRENCY` units as definition of symbol above.
* Total `amount` of the `ASSET` units as definition of symbol above.
* `fok` (fill or kill) -- if this order should either fill in its entirety or be completely aborted.
* `ioc` (immediate or cancel) -- if this order can be partially or completely filled, but any portion of the order that cannot be filled immediately will be canceled.
* `po` (post only) -- if you want this buy order to only be placed if no portion of it fills immediately.


```
client.limitBuy('BTC_LTC', '0.00685070', '32.6', ioc=True)
```

### Limit sell
Places a limit sell order in a given market. If successful, the method will return the order number.

Parameter | Mandatory
--------- | ---------
symbol | Yes
rate | Yes
amount | Yes
fok | No
ioc | No
po | No
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.
* The `rate` to purchase the `ASSET` in `CURRENCY` units as definition of symbol above.
* Total `amount` of the `ASSET` units as definition of symbol above.
* `fok` (fill or kill) -- if this order should either fill in its entirety or be completely aborted.
* `ioc` (immediate or cancel) -- if this order can be partially or completely filled, but any portion of the order that cannot be filled immediately will be canceled.
* `po` (post only) -- if you want this buy order to only be placed if no portion of it fills immediately.

```
client.limitSell('BTC_LTC', '0.00685070', '12.6')
```

### Market buy
The Poloniex REST API has not market orders from default. So this method is a limit buy order which emulates a market buy order.

Parameter | Mandatory
--------- | ---------
symbol | Yes
amount | Yes
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.
* The `rate` to purchase the `ASSET` in `CURRENCY` units as definition of symbol above.
* Total `amount` of the `ASSET` units as definition of symbol above.

```
client.marketBuy('BTC_LTC', '23.4432')
```

### Market sell
The Poloniex REST API has not market orders from default. So this method is a limit sell order which emulates a market sell order.

Parameter | Mandatory
--------- | ---------
symbol | Yes
amount | Yes
* Each `symbol` in Poloniex is written in capital letters as `CURRENCY_ASSET`. For instance `BTC_LTC`, `BTC` is used as currency to buy a given asset, `LTC`.
* The `rate` to purchase the `ASSET` in `CURRENCY` units as definition of symbol above.
* Total `amount` of the `ASSET` units as definition of symbol above.

```
client.marketSell('BTC_LTC', '120.12334')
```

### Cancel order
Cancels an order you have placed in a given market. If successful, the method will return a success of 1.

Parameter | Mandatory
--------- | ---------
symbol | Yes
order_number | Yes
* `symbol` of a given market written is capital letters.
* `order_number` is the identity number of the order to be canceled.

```
client.cancelOrder('BTC_DASH','514845991795')
```

### Cancel all orders
Cancels all open orders in a given market or, if no market is provided, all open orders in all markets. If successful, the method will return a success of 1 along with a json array of `orderNumbers` representing the orders that were canceled. Please note that `cancelAllOrders` can only be called 1 time per 2 minutes.

Parameter | Mandatory
--------- | ---------
symbol | No
* `symbol` of a given market written in capital letters.

```
client.cancelAllOrders()
```

### Withdraw
Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method, withdrawal privilege must be enabled for your API key.

Parameter | Mandatory
--------- | ---------
currency | Yes
amount | Yes
address | Yes
payment_id | No
currency_to_withdraw_as | No
* `currency` refers to abbreviation of a given asset name, e.g. `BTC` is the abbreviation of Bitcoin.
* Total `amount` of the `currency` units to withdraw.
* Your wallet `address`.
* For withdrawals which support payment IDs, (such as `XMR`) you may optionally specify `payment_id`.
* For currencies where there are multiple networks to choose from you need to specify the param: `currency_to_withdraw_as`. For `USDT` use `currency_to_withdraw_as`=`USDTTRON` or `USDTETH`. The default for `USDT` is Omni which is used if `currency_to_withdraw_as` is not specified.

```
client.withdraw('USDT', '456.54', 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t', currency_to_withdraw_as='USDTTRON')
```

### Deposit address
Coming soon.
### Generate new addresses
Coming soon.
### Deposits and withdraws history
Coming soon.

## Websocket methods
* The base endpoint is: wss://api2.poloniex.com
Coming soon.
