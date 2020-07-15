import config
import base64
import requests
import json
import csv

## https://www.espn.com/nfl/scoreboard/_/year/2019/seasontype/2/week/8 
## the page above has games that occured on 10-27-2019 that will be useful for easy testing

date = "20191110"
awayTeam = "ARI"
homeTeam = "TB"

gameParam = date + "-" + awayTeam + "-" + homeTeam

pullUrl = 'https://api.mysportsfeeds.com/v2.1/pull/nfl/2019-regular/games/' + gameParam + '/playbyplay.json'

returnDict = {}

##returnDict format: "team abbreviation" : [# of DEPs, yards from DEPs, # of DHPs, yards from DHPs, # of OPs, yards from OPs]
returnDict[homeTeam] = [0, 0, 0, 0, 0, 0]
returnDict[awayTeam] = [0, 0, 0, 0, 0, 0]

# Indices for penalty report
# 0 - Penalized Team 
# 1 - Penalty Type (DEP, DHP, OP)
# 2 - Yards from Penalty
# 3 - Pre-Penalty Field Position (Side of Field, Yardline)
# 4 - Enforced Penalty Field Position (Side of Field, Yardline)
# 5 - Post-Penalty Field Position (Side of Field, Yardline)
# 6 - Game clock (Quarter, time)
# 7 - Pre-Penalty Down & Distance (Down, Distance)

#List of penalty reports for the entire game
penaltyReport = []

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

    ##penalty data extraction
    for play in jsonResp["plays"]:
        keys = list(play.keys())
        print(play["description"])
        playType = keys[1]
        ##getting data from pre-snap fouls (offside, false start, illegal formation, etc.)
        if playType == "penalty":
            penalizedTeam = play[playType]["penalty"]["team"]["abbreviation"]
            teamInPoss = play["playStatus"]["teamInPossession"]["abbreviation"]
            yards = play[playType]["penalty"]["yardsPenalized"]

            if yards == 0:
                continue

            down = play["playStatus"]["currentDown"]
            yardsToGo = play["playStatus"]["yardsRemaining"]

            quarter = play["playStatus"]["quarter"]
            gameClock = 900 - play["playStatus"]["secondsElapsed"]
            time = (quarter, gameClock)

            sideOfField = play["playStatus"]["lineOfScrimmage"]["team"]["abbreviation"]
            yardLine = play["playStatus"]["lineOfScrimmage"]["yardLine"]

            ##down and distance tuple (down, yards remaining)
            downAndDistance =  (down, yardsToGo)

            ##field position tuple (side of field, yard line)
            preFieldPos = [sideOfField, yardLine]
            enforcedFieldPos = preFieldPos
            if play["description"] != "Neutral Zone Infraction":
                enforcedFieldPos = [play[playType]["penalty"]["enforcedAtPosition"]["team"]["abbreviation"], play[playType]["penalty"]["enforcedAtPosition"]["yardLine"]]
            postFieldPos = [sideOfField, yardLine]

            ## penalties on the offense (aka DHPs)
            if penalizedTeam == teamInPoss:
                ##DHP tally
                returnDict[penalizedTeam][2] += 1
                returnDict[penalizedTeam][3] += yards

                ##field position calculation
                if play[playType]["isNoPlay"] == True:
                    if sideOfField == teamInPoss:
                        postFieldPos[1] = enforcedFieldPos[1] - yards
                    else:
                        if yards + yardLine <= 50:
                            postFieldPos[1] = enforcedFieldPos[1] + yards
                        else:
                            postFieldPos[0] = teamInPoss
                            postFieldPos[1] = 100 - yards - enforcedFieldPos[1]
                else:
                    if sideOfField == teamInPoss:
                        postFieldPos[1] = enforcedFieldPos[1] - yards
                    else:
                        if yards + yardLine <= 50:
                            postFieldPos[1] = enforcedFieldPos[1] + yards
                        else:
                            postFieldPos[0] = teamInPoss
                            postFieldPos[1] = 100 - yards - enforcedFieldPos[1]

                ##add penalty to the report
                newPenalty = [penalizedTeam, "DHP", yards, preFieldPos, enforcedFieldPos, postFieldPos, time, downAndDistance]
                penaltyReport.append(newPenalty)

            ##penalties on the defense (aka DEPs or OPs)
            else:
                ##field position calculation
                if sideOfField != teamInPoss:
                    postFieldPos[1] = enforcedFieldPos[1] - yards
                else:
                    if yards + yardLine <= 50:
                        postFieldPos[1] = enforcedFieldPos[1] + yards
                    else:
                        postFieldPos[0] = penalizedTeam
                        postFieldPos[1] = 100 - yards + enforcedFieldPos[1]

                ##add penalty to the report
                newPenalty = [penalizedTeam, "", yards, preFieldPos, enforcedFieldPos, postFieldPos, time, downAndDistance]
               
                ##DEP tally
                if yards >= yardsToGo:
                    returnDict[penalizedTeam][0] += 1
                    returnDict[penalizedTeam][1] += yards
                    newPenalty[1] = "DEP"
                    penaltyReport.append(newPenalty)
                else:
                    returnDict[penalizedTeam][4] += 1
                    returnDict[penalizedTeam][5] += yards
                    newPenalty[1] = "OP"
                    penaltyReport.append(newPenalty)

        ##filters out XPA and 2pt conversions
        elif playType != "extraPointAttempt":
            #filters out other kickoffs and punts
            if playType == "kick":
                continue
            if playType == "punt":
                continue
            penaltiesOnThePlay = play[playType]["penalties"]
            for penalty in penaltiesOnThePlay:
                #skips offsetting penalties
                if type(penalty["penalty"]) is list:
                    ##print(play["description"])
                    ##print("got here\n")
                    continue
                penalizedTeam = penalty["penalty"]["team"]["abbreviation"]
                teamInPoss = play["playStatus"]["teamInPossession"]["abbreviation"]
                yards = penalty["penalty"]["yardsPenalized"]

                edgeCase = ["sack", "fieldGoalAttempt"]

                if playType not in edgeCase:
                    if yards == 0 or play[playType]["isTwoPointConversion"] == True:
                        continue
                elif yards == 0:
                    continue

                down = play["playStatus"]["currentDown"]
                yardsToGo = play["playStatus"]["yardsRemaining"]

                if down == None:
                    down = 1
                    yardsToGo = 10

                quarter = play["playStatus"]["quarter"]
                gameClock = 900 - play["playStatus"]["secondsElapsed"]
                time = (quarter, gameClock)

                sideOfField = ""
                yardLine = 9999
                if playType == "fieldGoalAttempt":
                    sideOfField = play[playType]["kickedFromPosition"]["team"]["abbreviation"]
                    yardLine = play[playType]["kickedFromPosition"]["yardLine"]
                else:
                    sideOfField = play["playStatus"]["lineOfScrimmage"]["team"]["abbreviation"]
                    yardLine = play["playStatus"]["lineOfScrimmage"]["yardLine"]

                ##down and distance
                downAndDistance =  (down, yardsToGo)

                ##field position tuple (side of field, yard line)
                preFieldPos = [sideOfField, yardLine]
                enforcedFieldPos = preFieldPos
                if penalty["penalty"]["enforcedAtPosition"] != None:
                    enforcedFieldPos = [penalty["penalty"]["enforcedAtPosition"]["team"]["abbreviation"], penalty["penalty"]["enforcedAtPosition"]["yardLine"]]
                postFieldPos = [sideOfField, yardLine]

                if penalizedTeam == teamInPoss:
                    returnDict[penalizedTeam][2] += 1
                    returnDict[penalizedTeam][3] += yards

                    ##field position calculation
                    if sideOfField == teamInPoss:
                        postFieldPos[1] = enforcedFieldPos[1] - yards
                    else:
                        if yards + yardLine <= 50:
                            postFieldPos[1] = enforcedFieldPos[1] + yards
                        else:
                            postFieldPos[0] = teamInPoss
                            postFieldPos[1] = 100 - yards - enforcedFieldPos[1] 
                    ##add penalty to the report
                    newPenalty = [penalizedTeam, "DHP", yards, preFieldPos, enforcedFieldPos, postFieldPos, time, downAndDistance]
                    penaltyReport.append(newPenalty)

                else:
                    ##field position calculation
                    if sideOfField != teamInPoss:
                        postFieldPos[1] = enforcedFieldPos[1] - yards
                    else:
                        if yards + yardLine <= 50:
                            postFieldPos[1] = enforcedFieldPos[1] + yards
                        else:
                            postFieldPos[0] = penalizedTeam
                            postFieldPos[1] = 100 - yards + enforcedFieldPos[1]

                    ##add penalty to the report
                    newPenalty = [penalizedTeam, "", yards, preFieldPos, enforcedFieldPos, postFieldPos, time, downAndDistance]

                    if yards >= yardsToGo:
                        returnDict[penalizedTeam][0] += 1
                        returnDict[penalizedTeam][1] += yards
                        newPenalty[1] = "DEP"
                    else:
                        returnDict[penalizedTeam][4] += 1
                        returnDict[penalizedTeam][5] += yards
                        newPenalty[1] = "OP"

                    penaltyReport.append(newPenalty)

    print(returnDict)
    ##print(penaltyReport)

    for penalty in penaltyReport:
        print(penalty)

except requests.exceptions.RequestException:
    print('HTTP Request failed')
