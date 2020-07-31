import os
import location
import teamList
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def tPEN_tEPC_graph(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

	seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

	seasonReportRaw.plot(x='Date',y=['tPEN(#)','tEPPfP'])

	plotLegend = plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)

	plotLegend.get_texts()[0].set_text('# of Penalties')
	plotLegend.get_texts()[1].set_text('EPC due to Penalties')

	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_tPENtEPPgraph.png",dpi=400)
	plt.clf()

def allExpPoints_graph(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

	seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

	seasonReportRaw.plot(x="Date",y=['tEPPfP','tEPDHP','tEPDEP','tEPDOP'])

	plotLegend = plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)

	plotLegend.get_texts()[0].set_text('EPC due to Penalties')
	plotLegend.get_texts()[1].set_text('EPC due to DHPs')
	plotLegend.get_texts()[2].set_text('EPC due to DEPs')
	plotLegend.get_texts()[3].set_text('EPC due to OPs')

	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_allExpPointsgraph.png",dpi=400)
	plt.clf()

def allPenalties_graph(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

	seasonReportRaw.plot(x="Date",y=['tPEN(#)','tDHP(#)','tDEP(#)','tOP(#)'])

	plotLegend = plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)

	plotLegend.get_texts()[0].set_text('# of Penalties')
	plotLegend.get_texts()[1].set_text('# of DHPs')
	plotLegend.get_texts()[2].set_text('# of DEPs')
	plotLegend.get_texts()[3].set_text('# of OPs')


	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_allPenaltiesgraph.png",dpi=400)
	plt.clf()

def allExpPoints_boxplot(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

	seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

	seasonReportRaw.boxplot(column=['tEPPfP','tEPDHP','tEPDEP','tEPDOP'])

	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_allExpPointsboxplot.png",dpi=400)
	plt.clf()

def allPenalties_boxplot(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

	seasonReportRaw.boxplot(column=['tPEN(#)','tDHP(#)','tDEP(#)','tOP(#)'])

	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_allPenaltiesboxplot.png",dpi=400)
	plt.clf()

def wins_tEPC_graph(year):
	seasonInfoDict = {}

	for team in teamList.teamList:
		directory = "C:/Users/" + location.location + "/Desktop/PenaltyStatsProject/Data/" + year + " " + team

		seasonInfoDict[team] = ()

		for filename in os.listdir(directory):
			csvLoc = directory + "/" + filename

			if filename != team + "_SeasonRaw.csv":
				continue

			seasonReportRaw = pd.read_csv(csvLoc)

			homewins = seasonReportRaw[(seasonReportRaw["Home Team"] == team) & (seasonReportRaw["Home Score"] > seasonReportRaw["Away Score"])]

			awaywins = seasonReportRaw[(seasonReportRaw["Away Team"] == team) & (seasonReportRaw["Away Score"] > seasonReportRaw["Home Score"])]

			totalwins = homewins["Home Team"].count() + awaywins["Away Team"].count()

			seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

			seasonInfoDict[team] = (totalwins, seasonReportRaw['tEPPfP'].sum())

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
	ax.plot(x,y,'ob')
	ax.plot(x1,y1,'-r')
	fig.subplots_adjust(bottom=0.3)
	fig.text(0.1,0.15,"r-value: " + str(r_value))
	fig.text(0.1,0.1,"r-squared value: " + str(r_value**2))
	plt.savefig("Analysis/Wins_vs_tEPP_graph.png",dpi=400)
	plt.clf()

def wins_tEPCPP_graph(year):
	seasonInfoDict = {}

	for team in teamList.teamList:
		directory = "C:/Users/" + 


if __name__ == '__main__':
	year = "19-20"
	
	wins_tEPC_graph(year)

	for team in teamList.teamList:
		allExpPoints_boxplot(year,team)
		allPenalties_boxplot(year,team)

		allExpPoints_graph(year,team)
		allPenalties_graph(year,team)

		tPEN_tEPC_graph(year,team)