import asyncio
import websockets
from time import sleep
import os, os.path


# Sends a request to the websocket server for the facial expression data
async def get_data():
    # ws://(uri):(portNo)
    # Port Number needs to match port number that is on the websocket
    uri = "ws://localhost:3000"
    async with websockets.connect(uri) as websocket:
        print("Making request for data")
        # Lists the number of files in the directory
        files = os.listdir('../../../ApexFiles/event/heartRate')
        facialFiles = os.listdir('../../../ApexFiles/event/facialRecog')
        if len(files) > 0:
            for heart in files:
                if os.path.exists('../../../ApexFiles/event/heartRate/' + heart):
                    file = open('../../../ApexFiles/event/heartRate/' + heart)
                    os.remove('../../../ApexFiles/event/heartRate/' + heart)
                    await websocket.send(file)
                    uri2 = "ws://localhost:4000"
                    async with websockets.connect(uri2) as websocket2:
                        data = await websocket2.recv()
                        print(data)

        if len(facialFiles) > 0:
            for face in facialFiles:
                if os.path.exists(
                        '../../../ApexFiles/event/facialRecog/' + face):
                    file = open('../../../ApexFiles/event/facialRecog/' + face)
                    os.remove('../../../ApexFiles/event/facialRecog/' + face)
                    await websocket.send(file)
                    uri2 = "ws://localhost:4000"
                    async with websockets.connect(uri2) as websocket2:
                        data = await websocket2.recv()
                        print(data)

        file = open('../../../ApexFiles/event/EventIn_GameContext.json')
        await websocket.send(file)
        uri2 = "ws://localhost:4000"
        async with websockets.connect(uri2) as websocket2:
            data = await websocket2.recv()
            print(data)


asyncio.get_event_loop().run_until_complete(get_data())
