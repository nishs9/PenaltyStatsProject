import os
import location
import teamList
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as numpy
from scipy import stats

##Scatterplot of Wins vs total expected points

for team in teamList.teamList:	
	directory = "C:/Users/" + location.location + "/Desktop/PenaltyStatsProject/Data/19-20 " + team 

	for filename in os.listdir(directory):
		csvLoc = directory + "/" + filename
		
		if filename != team + "_SeasonRaw.csv":
			continue
		
		seasonReportRaw = pd.read_csv(csvLoc)
		print(seasonReportRaw['tPEN(#)'].sum())

