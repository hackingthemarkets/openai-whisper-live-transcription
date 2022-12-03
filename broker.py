import redis, json
from ib_insync import *
import asyncio, time, random

# connect to Interactive Brokers 
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)
contract = Option('NVDA', '20221209', 160, 'C', 'SMART')
ib.qualifyContracts(contract)
ib.sleep(1)

order_placed = False

# connect to Redis and subscribe to speech messages
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe('textanalyzer')

async def check_messages():
    global order_placed

    print(f"{time.time()} - checking for messages")
    message = p.get_message()
    if message is not None and message['type'] == 'message':
        message_data = str(message['data'])
        if len(message_data) > 10:
            print(message)

            if 'moderate' in message_data and not order_placed:
                order = MarketOrder('BUY', 1)
                ib.placeOrder(contract, order)
                order_placed = True

async def run_periodically(interval, periodic_function):
    while True:
        await asyncio.gather(asyncio.sleep(interval), periodic_function())

asyncio.run(run_periodically(1, check_messages))

ib.run()