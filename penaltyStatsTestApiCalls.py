import config
import base64
import requests
import json
import csv

date = "20191027"
awayTeam = "NYG"
homeTeam = "DET"

##This script goes through play-by-play data and returns the total penalties and penalty yards for each team

gameParam = date + "-" + awayTeam + "-" + homeTeam

pullUrl = 'https://api.mysportsfeeds.com/v2.1/pull/nfl/2019-regular/games/' + gameParam + '/playbyplay.json'

returnDict = {}
returnDict[homeTeam] = [0, 0]
returnDict[awayTeam] = [0, 0]

try:
    response = requests.get(
        url= pullUrl,
        params={
            "fordate": date,
            "playtype": "penalty"
        },
        headers={
            "Authorization": "Basic " + base64.b64encode('{}:{}'.format(config.api_key,config.api_secret).encode('utf-8')).decode('ascii')
        }
    )
    print('Response HTTP Status Code: {status_code}'.format(
        status_code=response.status_code))
    jsonResp = response.json()
    respTxt = open("response.txt","w+")
    respTxt.write(json.dumps(jsonResp["plays"], indent=4))
    respTxt.close()
    ##print(len(jsonResp["plays"]))
    ##print(jsonResp["plays"][4].keys())

    for penalty in jsonResp["plays"]:
        keys = list(penalty.keys())
        playType = keys[1]
        if playType == "penalty":
            penalizedTeam = penalty[playType]["penalty"]["team"]["abbreviation"]
            yards = penalty[playType]["penalty"]["yardsPenalized"]
            returnDict[penalizedTeam][0] += 1
            returnDict[penalizedTeam][1] += yards
        else:
            penaltiesOnThePlay = penalty[playType]["penalties"]
            for penalty in penaltiesOnThePlay:
                if type(penalty["penalty"]) is list:
                    continue
                penalizedTeam = penalty["penalty"]["team"]["abbreviation"]
                yards = penalty["penalty"]["yardsPenalized"]
                returnDict[penalizedTeam][0] += 1
                returnDict[penalizedTeam][1] += abs(yards)

    print(returnDict)





except requests.exceptions.RequestException:
    print('HTTP Request failed')
