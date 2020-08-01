import os
import location
import teamList
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

##Scatterplot of Wins vs expected points per penalty


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

		totalwins = homewins["Home Team"].count() + awaywins["Away Team"].count()

		##print(str(homewins["Home Team"].count() + awaywins["Away Team"].count()))

		seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

		totalPens = seasonReportRaw['tPEN(#)'].sum()

		expPointsPerPen = seasonReportRaw['tEPPfP'].sum() / totalPens

		seasonInfoDict[team] = (totalwins, expPointsPerPen)

		##print(seasonReportRaw['tPEN(#)'].sum())
		##print(seasonReportRaw['tEPPfP'].sum())
		##print("\n")

##print(seasonInfoDict)

winsList = []
expPointsList = []

for team in seasonInfoDict.keys():
	winsList.append(seasonInfoDict[team][0])
	expPointsList.append(seasonInfoDict[team][1])

x = np.array(winsList)
y = np.array(expPointsList)

gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
mn = np.min(x)
mx = np.max(x)
x1 = np.linspace(mn,mx,500)
y1 = gradient*x1+intercept
fig,ax = plt.subplots(1)
##ax.plot(x,y,'ob')
ax.plot(x1,y1,'-r')
fig.subplots_adjust(bottom=0.3)
fig.text(0.1,0.15,"r-value: " + str(r_value))
fig.text(0.1,0.1,"r-squared value: " + str(r_value**2))
##plt.savefig("test.png",dpi=400)
plt.show()
plt.clf()
