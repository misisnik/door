import asyncio
from aiohttp import web
import aiohttp
import aiohttp_jinja2
import jinja2
import sockjs
import aiofiles
import os
import datetime
import json
import time
from functools import partial
from door import Door
from beacon import Beacon

_PATH = os.path.dirname(os.path.realpath(__file__))

# Database pro pokrocilejsi logovani
from models import Database
_db = Database()

_SESSION = None
# class for actual gpio (door lock/unlock, and buttons controll)
_DOOR = Door(_SESSION, _db)
# # bluetooth beacon initialization
# # BLE beacon scans will run in different thread
_BEACON = Beacon(_DOOR)
_BEACON.start()

async def websocket(msg, session):
    global _SESSION
    _SESSION = session
    try:
        if msg.tp == sockjs.MSG_CLOSED:
            try:
                pass
            except (KeyError, ValueError):
                pass
        elif msg.tp == sockjs.MSG_OPEN:
            session.manager.broadcast(json.dumps({'action':'msg', 'text': 'Someone joined'}))
            _DOOR._SESSION = session

        elif msg.tp == sockjs.MSG_MESSAGE:
            data = json.loads(msg.data)
            pass

    except:
        pass
        raise
loop = asyncio.get_event_loop()
app = web.Application(loop=loop)

path = os.path.join(os.path.dirname(__file__), 'templates')
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(path))

# initialize door and setup all all we need for controll

################################################################################
# REQUESTS
################################################################################

app.router.add_static('/static', _PATH+'/static')

# index
@partial(app.router.add_get, '/')
@aiohttp_jinja2.template('index.html')
async def main_page(request):
    pass

@partial(app.router.add_get, '/_api/door-state')
async def door_state(request):
    print('bylo uspesne pozadano o to jake maj dvere status jou')
    dt = _db.events.getAll().fetchall()
    # zones = _db.layers.get().fetchall()
    return web.json_response({'status': _DOOR.DOOR_STATE, 'data': dt})

@partial(app.router.add_post, '/_api/door-state')
async def set_door_state(request):
    # bylo uspesne pozadano o to aby se zmenil status dveri
    print('bylo upsesne pozadano o zmenu statusu')
    data = await request.json()
    print(data['status'])
    dt = _db.events.getAll().fetchall()
    dt = {'action':'loading', 'status': True, 'data': dt}
    try:
        _SESSION.manager.broadcast(json.dumps(dt))
    except Exception as e:
        print(e)

    # do actual thing due to state
    if data['status']:
        _DOOR.lock('Web')
    else:
        _DOOR.unlock('Web')
    # _db.layers.update(data['id'], position = json.dumps(data['position']))
    return web.json_response({'status': _DOOR.DOOR_STATE})

if __name__ == '__main__':
    sockjs.add_endpoint(app, prefix='/sockjs', handler=websocket)

    handler = app.make_handler()

    srv = loop.run_until_complete(
        loop.create_server(handler, '0.0.0.0', 8080))
    print("Server started at http://0.0.0.0:8080")
    # _db.device.insert('omron','omron',datetime.datetime.now().isoformat(), json.dumps([0,0]), json.dumps([]))
    # loop.create_task(olr.run())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        srv.close()
        loop.run_until_complete(handler.finish_connections())
