#!/usr/bin/env python
import time
import json
import asyncio
import aiohttp
from aiohttp_requests import requests
import calendar
from dateutil.parser import parse
from quart_cors import cors


initial = "0x0e98e6c1b32f61ed8396a11730ac2f7d46e9cb8b"
chain = []

async def watch_current():
    while True:
        prev = chain[-1] if chain else None
        current = prev['to'] if prev else initial

        print('check ' + current)
        response = await requests.get(f"https://api.zksync.io/api/v0.1/account/{current}/history/0/5")
        data = await response.json()
        
        for tx in data:
            #print(json.dumps(tx, indent=4))
            if tx['tx']['type'] == 'Transfer' and tx['tx']['from'] == current and tx['tx']['token'] == 'TBTC':
                print("found tx -> " + tx['tx']["to"])
                chain.append({
                    "from": tx['tx']["from"],
                    "to": tx['tx']["to"],
                    "amount": tx['tx']["amount"],
                    "fee": tx['tx']["fee"],
                    "tx_id": tx['tx_id'],
                    "date": tx['created_at'],
                    "timestamp": calendar.timegm(parse(tx['created_at']).timetuple()),
                })
                break

        await asyncio.sleep(30)



from quart import Quart

app = Quart(__name__)
app = cors(app, allow_origin="*")

@app.before_serving
async def create_db_pool():
    asyncio.ensure_future(watch_current())


@app.route('/torch')
async def torch():
    return json.dumps(chain)



app.run()
