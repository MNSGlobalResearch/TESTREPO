import asyncio
from ib_insync import *

def onPendingTickers(pendingTickers):
    global n1
    # n1 += sum(len(t.ticks) for t in pendingTickers)
    n1= len(pendingTickers)
    # n1 = sum(len(t.ticks) for t in pendingTickers)
    print(ib.wrapper.lastTime)
    print('A', n1)


async def coro():
    global n2
    while True:
        pendingTickers = await ib.pendingTickersEvent
        # n2 += sum(len(t.ticks) for t in pendingTickers)
        # n2 = sum(len(t.ticks) for t in pendingTickers)
        n2 = len(pendingTickers)
        print('B', n2)


async def coro2():
    global n3
    async for pendingTickers in ib.pendingTickersEvent:
        # n3 += sum(len(t.ticks) for t in pendingTickers)
        # n3 = sum(len(t.ticks) for t in pendingTickers)
        n3 = len(pendingTickers)
        print('C', n3)


async def coro3():
    global n4
    while True:
        await ib.updateEvent
        # n4 += sum(len(t.ticks) for t in ib.pendingTickers())
        # n4 = sum(len(t.ticks) for t in ib.pendingTickers())
        n4 = len(ib.pendingTickers())
        print('D', n4)


n1 = n2 = n3 = n4 = n5 = 0
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=200, timeout=30)
contracts = [
    Forex('EURSEK'),
    Forex('GBPNOK'),
    Forex('GBPSEK'),
    Forex('NOKSEK'),
    Forex('CHFNOK'),
    Forex('AUDNZD')]
    # Stock('SPY', 'SMART', 'USD'),
    # ContFuture("ES", exchange="GLOBEX", currency="USD")]
ib.qualifyContracts(*contracts)
tickers = [ib.reqMktData(c) for c in contracts]
ib.pendingTickersEvent += onPendingTickers
asyncio.ensure_future(coro())
asyncio.ensure_future(coro2())
asyncio.ensure_future(coro3())

while ib.waitOnUpdate():
    # this will miss ticks
    # n5 += sum(len(t.ticks) for t in tickers)
    # n5 = sum(len(t.ticks) for t in tickers)
    n5=len(tickers)
    print('E', n5)