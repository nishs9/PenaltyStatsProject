import os
import location
import teamList
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as numpy
from scipy.stats import linregress

##Scatterplot of Wins vs total expected points


## { 'Team' : (Wins,Total Expected Points) }
seasonInfoDict = {}

for team in teamList.teamList:	
	directory = "C:/Users/" + location.location + "/Desktop/PenaltyStatsProject/Data/19-20 " + team 

	seasonInfoDict[team] = ()

	for filename in os.listdir(directory):
		csvLoc = directory + "/" + filename
		
		if filename != team + "_SeasonRaw.csv":
			continue
		
		seasonReportRaw = pd.read_csv(csvLoc)

		homewins = seasonReportRaw[(seasonReportRaw["Home Team"] == team) & (seasonReportRaw["Home Score"] > seasonReportRaw["Away Score"])]

		awaywins = seasonReportRaw[(seasonReportRaw["Away Team"] == team) & (seasonReportRaw["Away Score"] > seasonReportRaw["Home Score"])]

		##print(str(homewins["Home Team"].count() + awaywins["Away Team"].count()))

		seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

		seasonInfoDict[team] = (homewins + awaywins, seasonReportRaw['tEPPFP'].sum())

		##print(seasonReportRaw['tPEN(#)'].sum())
		##print(seasonReportRaw['tEPPfP'].sum())
		print("\n")

