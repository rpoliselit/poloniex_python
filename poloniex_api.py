import aiohttp
import asyncio
import time
import hmac, hashlib
from urllib.parse import urlencode

def _create_timestamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

class poloniex:

    def __init__(self, APIkey=None, Secret=None):
        '''
        Client.
        '''
        self.APIkey = APIkey
        self.Secret = Secret

    def __repr__(self):
        signature = self.APIkey != None and self.Secret != None
        return "{}igned Poloniex API".format("S" if signature else "Uns")

    async def _response_status(self, response):
        if response.status == 200:
            return await response.json()
        elif response.status == 403:
            msg1 = 'MAINTENANCE MODE'
            msg2 = 'The exchange is currently under maintenance.'
            msg3 = 'Please check our poloniex Twitter feed for updates.'
            print(f"{msg1}\n{msg2}\n{msg3}")
            time.sleep(5*60)
        elif response.status == 500:
            print('Internal server error')
        elif response.status == 522:
            msg1 = 'CONNECTION ERROR'
            msg2 = 'Connection timed out'
            msg3 = ':CLOUDFLARE_ERROR_1000S_BOX:'
            print(f"{msg1}\n{msg2}\n{msg3}")
            time.sleep(60)
        elif response.status in [502, 504, 520]:
            msg1 = 'CONNECTION ERROR'
            msg2 = "Sorry, we're unable to connect to the server at the moment."
            msg3 = 'Please try again in a few minutes.'
            if response.status == 502:
                msg4 = 'Ray ID: 51bebe9bfe50cfe4'
            elif response.status == 504:
                msg4 = 'Ray ID: 5152b7813db7db78'
            elif response.status == 520:
                msg4 = 'Ray ID: 518639ac586fdbb4'
            print(f"{msg1}\n{msg2}\n{msg3}\n{msg4}")
            time.sleep(60)
        else:
            print(response.status)
            print(await response.text())

    async def _request(self, type, url, params={}, data={}, headers={}):
        async with aiohttp.ClientSession() as session:
            if type == 'GET':
                resp = await session.get(url, params=params)
            elif type == 'POST':
                resp = await session.post(url, data=data, headers=headers)
            return await self._response_status(resp)

    def _api_query(self, private_api=False, req={}):
        #public api url
        url_public = 'https://poloniex.com/public'
        #trading api url
        url_trade = 'https://poloniex.com/tradingApi'
        #websockets api url
        url_websocket = 'wss://api2.poloniex.com'

        if private_api == False:
            ret = self._request('GET', url_public, params=req)
        elif private_api == True:
            req['nonce'] = int(time.time()*1000)
            query_string = urlencode(req)
            post_data = query_string.encode("UTF-8")

            bkey = bytes(self.Secret, encoding="UTF-8")

            sign = hmac.new(bkey, post_data, hashlib.sha512).hexdigest()
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Sign': sign,
                'Key': self.APIkey
            }
            ret = self._request('POST', url_trade, data=query_string, headers=headers)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(ret)


# PUBLIC HTTP API METHODS:
    def rTicker(self, currency_pair=None, field=None):
        '''
        Retrieves summary information for each currency pair listed on the exchange.
        :currency_pair (optional): The currency pair e.g. 'BTC_LTC', 'BTC_DASH', etc...
        :field (optional): Information from a specific field, such as 'id', 'last', 'lowestAsk', 'highestBid', 'percentChange', 'baseVolume', 'quoteVolume', 'isFrozen', 'high24hr', and 'low24hr'.
        :return: Summery information as dict, or field information as float.
        '''
        req = {'command' : 'returnTicker'}
        ticker = self._api_query(False, req)
        if currency_pair != None:
            ticker = ticker[currency_pair]
            if field != None:
                ticker = float(ticker[field])
        return ticker

    def r24hVolume(self, currency_pair=None, currency=None):
        '''
        Returns the 24-hour volume for all markets as well as totals for primary currencies.
        :currency_pair (optional): The currency pair e.g. 'BTC_LTC', 'BTC_DASH', etc...
        :currency (optional): A given currency from pair.
        :return: The volume information as dict about currency pair, or specific currency volume as float.
        '''
        req = {'command' : 'return24hVolume'}
        volume = self._api_query(False, req)
        if currency_pair != None:
            volume = volume[currency_pair]
            if currency != None:
                volume = float(volume[currency])
        return volume

    def rOrderBook(self, currency_pair='all', depth=50, field=None):
        '''
        Returns the order book for a given market, as well as a sequence number used by websockets for synchronization of book updates and an indicator specifying whether the market is frozen. You may set currencyPair to "all" to get the order books of all markets.
        :currency_pair (default = 'all'): The currency pair e.g. 'BTC_LTC', 'BTC_DASH', etc...
        :depth (optional): Default depth is 50. Max depth is 100.
        :field (optional): Information from a specific field, such as 'asks', 'bids', 'isFrozen', and 'seq'.
        NOTE: Consider using the Websocket API over HTTP if you are looking for fresh and full order book depth.
        '''
        req = {
            'command' : 'returnOrderBook',
            'currencyPair': currency_pair,
            'depth': depth
        }
        order_book = self._api_query(False, req)
        if field != None and field in x:
            order_book = order_book[field]
            if field == 'asks' or field == 'bids':
                for elem in order_book:
                    for c, num in enumerate(elem):
                        elem[c] = float(num)
            else:
                order_book = int(order_book)
        return order_book

    def rMarketTradeHistory(self, currency_pair):
        '''
        Returns the past 200 trades for a given market.
        :currency_pair: The currency pair e.g. 'BTC_LTC', 'BTC_DASH', etc...
        '''
        req = {
            'command':'returnTradeHistory',
            'currencyPair': currency_pair
        }
        return self._api_query(False, req)

    def rChartData(self, currency_pair, start, period, end=None):
        '''
        Returns candlestick chart data.
        :currency_pair: A given currency pair e.g. 'BTC_LTC', 'BTC_DASH', etc...
        :start ("%Y-%m-%d %H:%M:%S"): The start of the window in seconds since the unix epoch.
        :period: Candlestick period in seconds. Valid values are 300, 900, 1800, 7200, 14400, and 86400.
        '''
        start = _create_timestamp(start)
        req = {
            'command': 'returnChartData',
            'currencyPair': currency_pair,
            'start': str(start),
            'period': str(period)
        }
        if end != None:
            end = _create_timestamp(end)
            req['end'] = str(end)
        return self._api_query(False, req)

    def rCurrencies(self, currency=None, field=None):
        '''
        Returns information about currencies.
        :currency (optional): A given currency e.g. 'BTC', 'LTC', 'XMR', etc...
        :field (optional): Information from a specific field, such as 'id', 'name', 'txFee', 'minConf', 'depositAddress', 'disabled', 'delisted', 'frozen', and 'isGeofenced'.
        '''
        req = {'command' : 'returnCurrencies'}
        coin = self._api_query(False, req)
        if currency != None:
            coin = coin[currency]
            if field == 'txFee':
                coin = float(coin[field])
            elif field != None:
                coin = coin[field]
        return coin

    def rLoanOrders(self, currency, field=None):
        '''
        Returns the list of loan offers and demands for a given currency.
        :currency: A given currency e.g. 'BTC', 'LTC', 'XMR', etc...
        :field (optional): Information from a specific field, such as 'offers' and 'demands'.
        '''
        req = {
            'command':'returnLoanOrders',
            'currency': currency
        }
        loan_orders = self._api_query(False, req)
        if field != None and loan_orders != None:
            loan_orders = loan_orders[field]
        return loan_orders


# TRADING API METHODS:
    def rBalances(self, currency=None):
        '''
        Returns all of your balances available for trade after having deducted all open orders.
        :currency (optional): A given currency e.g. 'BTC', 'LTC', 'XMR', etc...
        '''
        req = {'command':'returnBalances'}
        balances = self._api_query(True, req)
        if currency != None:
            balances = float(balances[currency])
        return balances

    def rCompleteBalances(self, currency=None, field=None):
        '''
        Returns all of your balances, including available balance, balance on orders, and the estimated BTC value of your balance.
        :currency (optional): A given currency e.g. 'BTC', 'LTC', 'XMR', etc...
        :field (optional): Information from a given field, such as 'available', 'onOrders', and 'btcValue'.
        '''
        req = {'command':'returnCompleteBalances'}
        balances = self._api_query(True, req)
        if currency != None:
            balances = balances[currency]
            if field != None:
                balances = float(balances[field])
        return balances

    def rOpenOrders(self, currency_pair='all'):
        '''
        Returns your open orders for a given market.
        :currency_pair (default = all): A given currency pair e.g. 'BTC_LTC', 'BTC_DASH', etc...
        '''
        req = {
            'command': 'returnOpenOrders',
            'currencyPair': currency_pair
        }
        return self._api_query(True, req)

    def rTradeHistory(self, currency_pair='all',start=None, end=None):
        '''
        Returns your trade history for a given market.
        :currency_pair (default = all): A given currency pair e.g. 'BTC_LTC', 'BTC_DASH', etc...
        :start (optional): "%Y-%m-%d %H:%M:%S"
        :end (optional): "%Y-%m-%d %H:%M:%S"
        '''
        req = {
            'command' : 'returnTradeHistory',
            'currencyPair' : currency_pair
        }
        if start != None:
            start = _create_timestamp(start)
            req['start'] = str(start)
        if end != None:
            end = _create_timestamp(end)
            req['end'] = str(end)
        return self._api_query(True, req)

    def limitBuy(self, currency_pair, rate, amount, fok=False, ioc=False, po=False):
        '''
        Places a limit buy order in a given market.
        :currency_pair: The major and minor currency defining the market where this sell order should be placed.
        :rate: The rate to purchase one major unit for this trade.
        :amount: The total amount of minor units offered in this sell order.
        :fok (optional): FILL OR KILL - Set to "True" if this order should either fill in its entirety or be completely aborted.
        :ioc (optional): IMMEDIATE OR CANCEL - Set to "True" if this order can be partially or completely filled, but any portion of the order that cannot be filled immediately will be canceled.
        :po (optional): POST ONLY - Set to "True" if you want this buy order to only be placed if no portion of it fills immediately.
        '''
        req = {
            'command' : 'buy',
            'currencyPair' : currency_pair,
            'rate' : rate,
            'amount' : amount
        }
        if fok == True:
            req['fillOrKill'] = '1'
        if ioc == True:
            req['immediateOrCancel'] = '1'
        if po == True:
            req['postOnly'] = '1'
        return self._api_query(True, req)

    def limitSell(self, currency_pair, rate, amount, fok=False, ioc=False, po=False):
        '''
        Places a sell order in a given market.
        :currency_pair: The major and minor currency defining the market where this sell order should be placed.
        :rate: The rate to purchase one major unit for this trade.
        :amount: The total amount of minor units offered in this sell order.
        :fok (optional): FILL OR KILL - Set to "True" if this order should either fill in its entirety or be completely aborted.
        :ioc (optional): IMMEDIATE OR CANCEL - Set to "True" if this order can be partially or completely filled, but any portion of the order that cannot be filled immediately will be canceled.
        :po (optional): POST ONLY - Set to "True" if you want this buy order to only be placed if no portion of it fills immediately.
        '''
        req = {
            'command' : 'sell',
            'currencyPair' : currency_pair,
            'rate' : rate,
            'amount' : amount
        }
        if fok == True:
            req['fillOrKill'] = '1'
        if ioc == True:
            req['immediateOrCancel'] = '1'
        if po == True:
            req['postOnly'] = '1'
        return self._api_query(True, req)

    def marketBuy(self, currency_pair, amount):
        """
        This is a limit order that tries to emulate a market order.
        """
        # calcular o rate num 'for'
        asks = self.rOrderBook(currency_pair=currency_pair, field='asks')
        list_resp = []
        for ask in asks:
            if ask[1] < amount:
                bought = self.limitBuy(currency_pair, rate=ask[0], amount=ask[1], ioc=True)
                list_resp.append(bought)
                amount -= ask[1]
            elif ask[1] >= amount:
                bought = self.limitBuy(currency_pair, rate=ask[0], amount=amount, ioc=True)
                list_resp.append(bought)
                amount -= amount
                break
        return list_resp

    def marketSell(self, currency_pair, amount):
        """
        This is a limit order that tries to emulate a market order.
        """
        # calcular o rate num 'for'
        bids = rOrderBook(currency_pair=currency_pair, field='bids')
        list_resp = []
        for bid in bids:
            if bid[1] < amount:
                sold = self.limitSell(currency_pair, rate=bid[0], amount=bid[1], ioc=True)
                list_resp.append(sold)
                amount -= bid[0]
            elif bid[1] >= amount:
                sold = self.limitSell(currency_pair, rate=bid[0], amount=amount, ioc=True)
                list_resp.append(sold)
                amount -= amount
                break
        return list_resp

    def cancelOrder(self, currency_pair, order_number):
        '''
        Cancels an order you have placed in a given market.
        :currency_pair: The major and minor currency defining the market where this sell order should be placed.
        :order_Number: The identity number of the order to be canceled.
        '''
        req = {
            'command' : 'cancelOrder',
            'currencyPair' : currency_pair,
            'orderNumber' : str(order_number)
        }
        return self._api_query(True, req)

    def cancelAllOrders(self, currency_pair=None):
        '''
        Cancels all open orders in a given market or, if no market is provided, all open orders in all markets.
        :currency_pair (optional): The base and quote currency that define a market.
        '''
        req = {'command' : 'cancelAllOrders'}
        if currency_pair != None:
            req['currencyPair'] = currency_pair
        return self._api_query(True, req)

    def withdraw(self, currency, amount, address, payment_id=None, currency_to_withdraw_as=None):
        '''
        Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method, withdrawal privilege must be enabled for your API key.
        '''
        req = {
            'command' : 'withdraw',
            'currency' : currency,
            'amount' : str(amount),
            'address' : address
        }
        if payment_id != None:
            req['paymentId'] = str(payment_id)
        if currencyToWithdrawAs != None:
            req['currencyToWithdrawAs'] = currency_to_withdraw_as
        return _api_query(True, req)


# WEBSOCKETS API METHODS
    def wsTicker(self):
        req = {'command':'subscribe', 'chanel':1002}
        # return self._api_query(private_api='WS', req=req)

    def ws24hVolume(self):
        req = {'command':'subscribe', 'chanel':1003}

    def wsHeartbeats(self):
        req = {'command':'subscribe', 'chanel':1010}

    def wsPriceAggBook(self, currency_pair):
        req = {'command':'subscribe', 'chanel':currency_pair}
