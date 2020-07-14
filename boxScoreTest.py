import config
import base64
import requests
import json
import csv

date = "20191209"
awayTeam = "NYG"
homeTeam = "PHI"

gameParam = date + "-" + awayTeam + "-" + homeTeam


# Indices for score report
# 0 - home team score 
# 1 - away team score
# 2 - quarter
# 3 - time

#List of individual score reports for the entire game
scoreReport = []
numScores = len(scoreReport)

try:
    response = requests.get(
        url='https://api.mysportsfeeds.com/v2.1/pull/nfl/2019-regular/games/' + gameParam + '/boxscore.json',
        params={
            "fordate": date
        },
        headers={
            "Authorization": "Basic " + base64.b64encode('{}:{}'.format(config.api_key,config.api_secret).encode('utf-8')).decode('ascii')
        }
    )
    print('Response HTTP Status Code: {status_code}'.format(
        status_code=response.status_code))
    jsonResp = response.json()
    respTxt = open("boxscoreresponse.txt","w+")
    respTxt.write(json.dumps(jsonResp, indent=4))
    respTxt.close()

    ##store final score
    finalScore = {}
    finalScore[homeTeam] = jsonResp["scoring"]["homeScoreTotal"]
    finalScore[awayTeam] = jsonResp["scoring"]["awayScoreTotal"]

    currQuarter = 1

    numQuarter = len(jsonResp["scoring"]["quarters"])

    while currQuarter < numQuarter + 1:
        scoringPlays = jsonResp["scoring"]["quarters"][currQuarter - 1]["scoringPlays"]
        for scoringPlay in scoringPlays:
            newScore = []
            if numScores == 0:
                newScore = [0,0,currQuarter,0]
            else:
                newScore = [scoreReport[numScores - 1][0], scoreReport[numScores - 1][1], currQuarter, 0]

            homeScore = newScore[0] + scoringPlay["homeScore"]
            awayScore = newScore[1] + scoringPlay["awayScore"]

            newScore[0] = homeScore
            newScore[1] = awayScore
            newScore[3] = 900 - scoringPlay["quarterSecondsElapsed"]

            scoreReport.append(newScore)


        currQuarter += 1

    print(scoreReport)


except requests.exceptions.RequestException:
    print('HTTP Request failed')
