import config
import base64
import requests
import json


## list of tuples (week #, date, home team, away team)
scheduleList = []

try:
    response = requests.get(
        url="https://api.mysportsfeeds.com/v2.1/pull/nfl/2019-regular/games.json",
        params={
            "fordate": "20200716",
            "team": "WAS"
        },
        headers={
            "Authorization": "Basic " + base64.b64encode('{}:{}'.format(config.api_key,config.api_secret).encode('utf-8')).decode('ascii')
        }
    )
    print('Response HTTP Status Code: {status_code}'.format(
        status_code=response.status_code))
    jsonResp = response.json()
    games = jsonResp["games"]

    for game in games:
        weekNumber = game["schedule"]["week"]

        rawDate = game["schedule"]["startTime"][:10]
        listDate = rawDate.split("-")
        date = listDate[0] + listDate[1] + listDate[2]

        awayTeam = game["schedule"]["awayTeam"]["abbreviation"]
        homeTeam = game["schedule"]["homeTeam"]["abbreviation"]

        gameTup = (weekNumber, date, awayTeam, homeTeam)
        scheduleList.append(gameTup)


    for schedule in scheduleList:
        print(schedule)



except requests.exceptions.RequestException:
    print('HTTP Request failed')