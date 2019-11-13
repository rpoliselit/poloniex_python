from poloniex_api import poloniex
import keys
api = keys.poloniex_apikey
secret = keys.poloniex_secret

# client = poloniex()
client = poloniex(api, secret)
print(client)

#public api methods
# print(client.rTicker('BTC_LTC', 'last'))
# print(client.r24hVolume('BTC_LTC', 'LTC'))
# print(client.rOrderBook('BTC_LTC', 4, 'asks'))
# print(client.rMarketTradeHistory('BTC_LTC'))
# print(client.rChartData('BTC_LTC', '2019-08-18 18:45:00', 300))
# print(client.rCurrencies('BTC', 'txFee'))
# print(client.rLoanOrders('BTC','demands'))

#trading api methods
# print(client.rBalances('BTC'))
# print(client.rCompleteBalances('BTC', 'available'))
print(client.rOpenOrders('BTC_LTC'))
# print(client.rTradeHistory())
# print(client.buy())
# print(client.sell())
# print(client.cancelOrder())
# print(client.cancelAllOrders())
# print(client.withdraw())

#websockets api methods
