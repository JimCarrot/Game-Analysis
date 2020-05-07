import fitbit
import gather_keys_oauth2 as Oauth2
import json
import asyncio
from datetime import datetime


# Sends the heart rate data to the websocket server to be stored
async def send_data(data):
    uri = "ws://localhost:12345"
    async with websockets.connect(uri) as websocket:
        json_file = open("../../../ApexFiles/event/EventIn_BoozeItem_101433CET_thurs.json")
        print(json_file)
        # await websocket.send(json.dumps(str(data)))
        # await websocket.send(json)


# Getting the client's id and secret key
client_id = '22BJS6'
client_secret = '7ac70f93fd408169359ce06499d1f402'

# Authenticating the id and secret key to get authorization to use the fit bit API
server = Oauth2.OAuth2Server(client_id, client_secret)
server.browser_authorize()

# Getting the access token and refresh token to be able to retrieve the heart rate for a particular date
access_token = str(server.fitbit.client.session.token['access_token'])
refresh_token = str(server.fitbit.client.session.token['refresh_token'])

# Retrieving the fit bit data from a particular date
auth2_client = fitbit.Fitbit(client_id, client_secret, oauth2=True, access_token=access_token,
                             refresh_token=refresh_token)

date = datetime.today().strftime('%Y-%m-%d')

fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=date, detail_level='1sec')

heart_rate = {
    "nameSpace": "heartrate.com",
    "name": "heartRateEvent",
    "version": "0.0.1"
}
heartRateVariables = ""
index = 1
fileIndex = 0
for hr in fit_statsHR['activities-heart-intraday']['dataset']:
    if index % 35 == 0:
        heart_rate['heartRateVariables'] = heartRateVariables
        with open('../../../ApexFiles/event/heartRate/EventIn_HeartRate' + str(fileIndex) + '.json', 'w') as file:
            json.dump(heart_rate, file)
        fileIndex += 1
        index = 1
    else:
        heartRateVariables += str(hr['time']) + "/" + str(hr['value']) + ","
        index += 1
