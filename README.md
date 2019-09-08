# poloniex_python
Module to use the Poloniex Exchange API with python.

Its is recommended to touch a keys.py that contains you poloniex credentials.

from poloniexAPI import poloniex
import keys

## 1 - Client

client = poloniex(keys.api, keys.secret)

## 2 - Public methods
Theses methods work without signature.

### 2.1 - rTicker

client.rTicker()

## 3 - Trade methods
Only theses methods needs signature.

## 4 - Websocket methods
