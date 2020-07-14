import config
import base64
import requests
import json
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select

## returns a tuple with the cumulative penalty info and penalty report
def penaltyReport(date, awayTeam, homeTeam):
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
	# 3 - Pre-Penalty Field Position
	# 4 - Enforced Penalty Field Position 
	# 5 - Post-Penalty Field Position 
	# 6 - Game clock (Quarter, time)
	# 7 - Pre-Penalty Down & Distance

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
			##print(play["description"])
			playType = keys[1]
			##getting data from pre-snap fouls (offside, false start, illegal formation, etc.)
			if playType == "penalty":
				penalizedTeam = play[playType]["penalty"]["team"]["abbreviation"]
				teamInPoss = play["playStatus"]["teamInPossession"]["abbreviation"]
				yards = play[playType]["penalty"]["yardsPenalized"]

				if yards == 0:
					continue

				## getting basic game state information
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
							postFieldPos[1] = 100 - yards - enforcedFieldPos[1]

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

			##filters out XPA, 2pt conversions, kickoffs and punts
			elif playType != "extraPointAttempt":
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

					#checks for a 2pt conversion or declined penalty
					if playType != "sack":
						if yards == 0 or play[playType]["isTwoPointConversion"] == True:
							continue
					elif yards == 0:
						continue

					## getting basic game state information
					down = play["playStatus"]["currentDown"]
					yardsToGo = play["playStatus"]["yardsRemaining"]

					quarter = play["playStatus"]["quarter"]
					gameClock = 900 - play["playStatus"]["secondsElapsed"]
					time = (quarter, gameClock)

					sideOfField = play["playStatus"]["lineOfScrimmage"]["team"]["abbreviation"]
					yardLine = play["playStatus"]["lineOfScrimmage"]["yardLine"]

					##down and distance
					downAndDistance =  (down, yardsToGo)

					##field position tuple (side of field, yard line)
					preFieldPos = [sideOfField, yardLine]
					enforcedFieldPos = [penalty["penalty"]["enforcedAtPosition"]["team"]["abbreviation"], penalty["penalty"]["enforcedAtPosition"]["yardLine"]]
					postFieldPos = [sideOfField, yardLine]

					## offensive penalty (DHP)
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
								postFieldPos[1] = 100 - yards - enforcedFieldPos[1]

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

		##print(returnDict)
		##print(penaltyReport)

		##for penalty in penaltyReport:
			##print(penalty)

		returnTup = (returnDict, penaltyReport)
		return returnTup

	except requests.exceptions.RequestException:
		print('HTTP Request failed')
		return None

def boxScoreReport(date, awayTeam, homeTeam):
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

		return scoreReport


	except requests.exceptions.RequestException:
		print('HTTP Request failed')

def expectedPointsCalc(awayTeam, homeTeam, penaltyReport, boxScoreInfo):
	## intializing the web-scraping phase of the function
	chromedriver_location = "C:/Users/analy/Downloads/chromedriver_win32/chromedriver"
	driver = webdriver.Chrome(chromedriver_location)

	returnList = []

	for penalty in penaltyReport:
		teamInPoss = ""
		penalizedTeam = penalty[0]
		penaltyType = penalty[1]
		preFieldPos = penalty[3]
		postFieldPos = penalty[5]
		quarter = penalty[6][0]
		clock = penalty[6][1]
		down = penalty[7][0]
		distance = penalty[7][1]
		scoreDifferential = 0

		if down == 0:
			down = 1
		if distance == 0:
			distance = 10

		## figuring out who was in possession of the ball during the penalty
		if penaltyType == "DHP":
			if penalizedTeam == awayTeam:
				teamInPoss = "awayTeam"
			else:
				teamInPoss = "homeTeam"
		else:
			if penalizedTeam == awayTeam:
				teamInPoss = "homeTeam"
			else:
				teamInPoss = "awayTeam"

		## figuring out the score differential at the time of the penalty
		i = 0
		for score in boxScoreInfo:
			## edge cases
			if quarter < score[2]:
				if i == 0:
					scoreDifferential = 0
				else:
					if teamInPoss == "awayTeam":
						scoreDifferential = boxScoreInfo[i-1][1] - boxScoreInfo[i-1][0]
					else:
						scoreDifferential = boxScoreInfo[i-1][0] - boxScoreInfo[i-1][1]
			elif quarter > score[2]:
				continue
			else:
				if clock > score[3]:
					if teamInPoss == "awayTeam":
						scoreDifferential = boxScoreInfo[i-1][1] - boxScoreInfo[i-1][0]
					else:
						scoreDifferential = boxScoreInfo[i-1][0] - boxScoreInfo[i-1][1]
			i += 1  

		## NOTE: This calculator takes everything into account from the team in possession's perspective 
		driver.get("https://www.pro-football-reference.com/play-index/win_prob.cgi")

		## Each of the form fields/buttons
		score_diff = '//*[@id="wp_calc"]/div/div[1]/div[1]/input'
		time_min = '//*[@id="wp_calc"]/div/div[1]/div[4]/input[1]'
		time_sec = '//*[@id="wp_calc"]/div/div[1]/div[4]/input[2]'
		side_of_field = '//*[@id="field"]'
		yard_line = '//*[@id="wp_calc"]/div/div[1]/div[5]/input'
		yards_to_go = '//*[@id="wp_calc"]/div/div[1]/div[7]/input'
		submit = '//*[@id="wp_calc"]/div/div[2]/div/input'

		preExpPts = 0

		driver.find_element_by_xpath(score_diff).send_keys(str(scoreDifferential))
		driver.find_element_by_xpath('//*[@id="wp_calc"]/div/div[1]/div[3]/div[' + str(quarter) + ']/div[1]/input').click()
		driver.find_element_by_xpath(time_min).send_keys(str(int(clock/60)))
		driver.find_element_by_xpath(time_sec).send_keys(str(clock%60))

		if teamInPoss == "awayTeam":
			if awayTeam == preFieldPos[0]:
				select = Select(driver.find_element_by_xpath(side_of_field))
				select.select_by_visible_text("Team")
			else:
				select = Select(driver.find_element_by_xpath(side_of_field))
				select.select_by_visible_text("Opp")
		else:
			if homeTeam == preFieldPos[0]:
				select = Select(driver.find_element_by_xpath(side_of_field))
				select.select_by_visible_text("Team")
			else:
				select = Select(driver.find_element_by_xpath(side_of_field))
				select.select_by_visible_text("Opp")

		driver.find_element_by_xpath(yard_line).send_keys(str(preFieldPos[1]))
		driver.find_element_by_xpath('//*[@id="wp_calc"]/div/div[1]/div[6]/div[' + str(down) + ']/div[1]/input').click()
		driver.find_element_by_xpath(yards_to_go).send_keys(str(distance))

		driver.find_element_by_xpath(submit).click()

		preExpPts = driver.find_element_by_xpath('//*[@id="pi"]/div[2]/h3[1]').text

		postExpPts = 0

		driver.get("https://www.pro-football-reference.com/play-index/win_prob.cgi")

		driver.find_element_by_xpath(score_diff).send_keys(str(scoreDifferential))
		driver.find_element_by_xpath('//*[@id="wp_calc"]/div/div[1]/div[3]/div[' + str(quarter) + ']/div[1]/input').click()
		driver.find_element_by_xpath(time_min).send_keys(str(int(clock/60)))
		driver.find_element_by_xpath(time_sec).send_keys(str(clock%60))

		if teamInPoss == "awayTeam":
			if awayTeam == postFieldPos[0]:
				select = Select(driver.find_element_by_xpath(side_of_field))
				select.select_by_visible_text("Team")
			else:
				select = Select(driver.find_element_by_xpath(side_of_field))
				select.select_by_visible_text("Opp")
		else:
			if homeTeam == postFieldPos[0]:
				select = Select(driver.find_element_by_xpath(side_of_field))
				select.select_by_visible_text("Team")
			else:
				select = Select(driver.find_element_by_xpath(side_of_field))
				select.select_by_visible_text("Opp")

		driver.find_element_by_xpath(yard_line).send_keys(str(postFieldPos[1]))
		driver.find_element_by_xpath('//*[@id="wp_calc"]/div/div[1]/div[6]/div[' + str(down) + ']/div[1]/input').click()
		driver.find_element_by_xpath(yards_to_go).send_keys(str(distance))

		driver.find_element_by_xpath(submit).click()

		postExpPts = driver.find_element_by_xpath('//*[@id="pi"]/div[2]/h3[1]').text

		expPtsAdded = float(postExpPts.split(" ")[2]) - float(preExpPts.split(" ")[2])

		returnList.append([penalizedTeam, preExpPts.split(" ")[2], postExpPts.split(" ")[2], expPtsAdded])


	driver.close()
	return returnList

def csvIfy(date,awayTeam,homeTeam,boxScoreInfo,cumulPenInfo,penaltyReport,expPointReport):
	homeScore = boxScoreInfo[len(boxScoreInfo)-1][0]
	awayScore = boxScoreInfo[len(boxScoreInfo)-1][1]

	csvFileName = date + "-" + awayTeam + "-" + homeTeam + ".csv"

	infoSectionHeader = ["Date","Home Team", "Home Score", "Away Team", "Away Score"]
	infoSection = [date, homeTeam, homeScore, awayTeam, awayScore]
	section1Header = ["Team", "Type", "Yards", "Pre-EP", "Post-EP", "Diff-EP"]
	section1 = []
	section2Header = ["Team", "tPEN(#)", "tPEN(yards)", "tDHP(#)", "tDHP(yards)", "tEPDHP", "tDEP(#)", "tDEP(yards)", "tEPDEP","tOP(#)", "tOP(yards)", "tEPOP"]
	section2 = []
	section3Header = ["Team", "Yards/Pen", "Yards/DHP", "EP/DHP", "Yards/DEP", "EP/DEP", "Yards/OP", "EP/OP"]
	section3 = []

	i = 0
	while i < len(penaltyReport):
		currRow = [penaltyReport[i][0],penaltyReport[i][1],penaltyReport[i][2],expPointReport[i][1],expPointReport[i][2],expPointReport[i][3]]
		section1.append(currRow)
		i += 1

	home_totalPens = 0
	home_totalYards = 0
	home_tEPDHP = 0
	home_tEPDEP = 0
	home_tEPOP = 0

	away_totalPens = 0
	away_totalYards = 0
	away_tEPDHP = 0
	away_tEPDEP = 0
	away_tEPOP = 0

	for row in section1:
		if row[0] == awayTeam:
			away_totalPens += 1
			away_totalYards += row[2]
			if row[1] == "DHP":
				away_tEPDHP += row[5]
			elif row[1] == "DEP":
				away_tEPDEP += row[5]
			else:
				away_tEPOP += row[5]
		else:
			home_totalPens += 1
			home_totalYards += row[2]
			if row[1] == "DHP":
				home_tEPDHP += row[5]
			elif row[1] == "DEP":
				home_tEPDEP += row[5]
			else:
				home_tEPOP += row[5]

	section2.append([homeTeam, home_totalPens, home_totalYards, cumulPenInfo[homeTeam][2], cumulPenInfo[homeTeam][3], home_tEPDHP, cumulPenInfo[homeTeam][0], cumulPenInfo[homeTeam][1], home_tEPDEP, cumulPenInfo[homeTeam][4], cumulPenInfo[homeTeam][5], home_tEPOP])
	section2.append([awayTeam, away_totalPens, away_totalYards, cumulPenInfo[awayTeam][2], cumulPenInfo[awayTeam][3], away_tEPDHP, cumulPenInfo[awayTeam][0], cumulPenInfo[awayTeam][1], away_tEPDEP, cumulPenInfo[awayTeam][4], cumulPenInfo[awayTeam][5], away_tEPOP])

	home_yardsPerPen = "N/A"
	if home_totalPens > 0:
		home_yardsPerPen = home_totalYards/home_totalPens
	
	home_yardsPerDHP = "N/A"
	home_expPointsPerDHP = "N/A"
	if cumulPenInfo[homeTeam][2] > 0:
		home_yardsPerDHP = cumulPenInfo[homeTeam][3]/cumulPenInfo[homeTeam][2]
		home_expPointsPerDHP = home_tEPDHP/cumulPenInfo[homeTeam][2]
	
	home_yardsPerDEP = "N/A"
	home_expPointsPerDEP = "N/A"
	if cumulPenInfo[homeTeam][0] > 0:
		home_yardsPerDEP = cumulPenInfo[homeTeam][1]/cumulPenInfo[homeTeam][0]
		home_expPointsPerDEP = home_tEPDEP/cumulPenInfo[homeTeam][0]
	
	home_yardsPerOP = "N/A"
	home_expPointsPerOP = "N/A"
	if cumulPenInfo[homeTeam][4] > 0:
		home_yardsPerOP = cumulPenInfo[homeTeam][5]/cumulPenInfo[homeTeam][4]
		home_expPointsPerOP = home_tEPOP/cumulPenInfo[homeTeam][4]

	away_yardsPerPen = "N/A"
	if away_totalPens > 0:
		away_yardsPerPen = away_totalYards/away_totalPens
	
	away_yardsPerDHP = "N/A"
	away_expPointsPerDHP = "N/A"
	if cumulPenInfo[awayTeam][2] > 0:
		away_yardsPerDHP = cumulPenInfo[awayTeam][3]/cumulPenInfo[awayTeam][2]
		away_expPointsPerDHP = away_tEPDHP/cumulPenInfo[awayTeam][2]
	
	away_yardsPerDEP = "N/A"
	away_expPointsPerDEP = "N/A"
	if cumulPenInfo[awayTeam][0] > 0:
		away_yardsPerDEP = cumulPenInfo[awayTeam][1]/cumulPenInfo[awayTeam][0]
		away_expPointsPerDEP = away_tEPDEP/cumulPenInfo[awayTeam][0]
	
	away_yardsPerOP = "N/A"
	away_expPointsPerOP = "N/A"
	if cumulPenInfo[awayTeam][4] > 0:
		away_yardsPerOP = cumulPenInfo[awayTeam][5]/cumulPenInfo[awayTeam][4]
		away_expPointsPerOP = away_tEPOP/cumulPenInfo[awayTeam][4]

	section3.append([homeTeam, home_yardsPerPen, home_yardsPerDHP, home_expPointsPerDHP, home_yardsPerDEP, home_expPointsPerDEP, home_yardsPerOP, home_expPointsPerOP])
	section3.append([awayTeam, away_yardsPerPen, away_yardsPerDHP, away_expPointsPerDHP, away_yardsPerDEP, away_expPointsPerDEP, away_yardsPerOP, away_expPointsPerOP])

	with open(csvFileName, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(infoSectionHeader)
		writer.writerow(infoSection)
		writer.writerow(section1Header)

		for row in section1:
			writer.writerow(row)

		writer.writerow([])
		writer.writerow(section2Header)
		for row in section2:
			writer.writerow(row)

		writer.writerow([])
		writer.writerow(section3Header)
		for row in section3:
			writer.writerow(row)

	print("CSVified!")

if __name__ == '__main__':
	date = "20190915"
	awayTeam = "PHI"
	homeTeam = "ATL"

	penaltyInfoTup = penaltyReport(date, awayTeam, homeTeam)
	boxScoreInfo = boxScoreReport(date, awayTeam, homeTeam)
	
	cumulPenInfo = penaltyInfoTup[0]
	penaltyReport = penaltyInfoTup[1]
	expPointReport = expectedPointsCalc(awayTeam, homeTeam, penaltyReport, boxScoreInfo)

	csvIfy(date,awayTeam,homeTeam,boxScoreInfo,cumulPenInfo,penaltyReport,expPointReport)

	for penalty in penaltyReport:
		print(penalty)

	print("\n")

	for expPoint in expPointReport:
		print(expPoint)
