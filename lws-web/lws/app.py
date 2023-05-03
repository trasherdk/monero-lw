import asyncio
from quart import Quart, websocket, render_template, jsonify

from lws.broker import Broker
from lws.models import Message


app = Quart(__name__)
broker = Broker()


def run() -> None:
    app.run()


@app.get('/') 
async def index():
    return await render_template("index.html")


@app.get('/replay')
async def replay():
    data = list()
    messages = Message.select().order_by(Message.datestamp.asc()).limit(100)
    for m in messages:
        data.append({
            'message': m.message,
            'datestamp': m.datestamp
        })
    return jsonify(data)


@app.websocket('/ws')
async def ws() -> None:
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    finally:
        task.cancel()
        await task


async def _receive() -> None:
    while True:
        message = await websocket.receive()
        if len(message) > 120:
            print('too long, skipping')
            break
        await broker.publish(message)