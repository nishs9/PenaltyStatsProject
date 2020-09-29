import os
import location
import teamList
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def penaltySummary_table(year, team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")
	seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

	homeWins = seasonReportRaw[(seasonReportRaw["Home Team"] == team) & (seasonReportRaw["Home Score"] > seasonReportRaw["Away Score"])]
	awayWins = seasonReportRaw[(seasonReportRaw["Away Team"] == team) & (seasonReportRaw["Away Score"] > seasonReportRaw["Home Score"])]

	homeLosses = seasonReportRaw[(seasonReportRaw["Home Team"] == team) & (seasonReportRaw["Home Score"] < seasonReportRaw["Away Score"])]
	awayLosses = seasonReportRaw[(seasonReportRaw["Away Team"] == team) & (seasonReportRaw["Away Score"] < seasonReportRaw["Home Score"])]

	winCount = homeWins["Home Team"].count() + awayWins["Away Team"].count()

	PenaltiesSeasonTotal = seasonReportRaw["tPEN(#)"].sum()
	PenaltiesSeasonAverage = PenaltiesSeasonTotal / 16
	PenaltiesWinTotal = homeWins["tPEN(#)"].sum() + awayWins["tPEN(#)"].sum()
	PenaltiesWinAverage = PenaltiesWinTotal / winCount
	PenaltiesLossTotal = homeLosses["tPEN(#)"].sum() + awayLosses["tPEN(#)"].sum()
	PenaltiesLossAverage = PenaltiesLossTotal / (16-winCount)

	EPCSeasonTotal = seasonReportRaw["tEPPfP"].sum()
	EPCSeasonAverage = EPCSeasonTotal / 16
	EPCWinTotal = homeWins["tEPPfP"].sum() + awayWins["tEPPfP"].sum()
	EPCWinAverage = EPCWinTotal / winCount
	EPCLossTotal = homeLosses["tEPPfP"].sum() + awayLosses["tEPPfP"].sum()
	EPCLossAverage = EPCLossTotal / (16-winCount)

	EPCDHPSeasonTotal = seasonReportRaw["tEPDHP"].sum()
	EPCDHPSeasonAverage = EPCDHPSeasonTotal / 16
	EPCDHPWinTotal = homeWins["tEPDHP"].sum() + awayWins["tEPDHP"].sum()
	EPCDHPWinAverage = EPCDHPWinTotal / winCount
	EPCDHPLossTotal = homeLosses["tEPDHP"].sum() + awayLosses["tEPDHP"].sum()
	EPCDHPLossAverage = EPCDHPLossTotal / (16-winCount)

	EPCDEPSeasonTotal = seasonReportRaw["tEPDEP"].sum()
	EPCDEPSeasonAverage = EPCDEPSeasonTotal / 16
	EPCDEPWinTotal = homeWins["tEPDEP"].sum() + awayWins["tEPDEP"].sum()
	EPCDEPWinAverage = EPCDEPWinTotal / winCount
	EPCDEPLossTotal = homeLosses["tEPDEP"].sum() + awayLosses["tEPDEP"].sum()
	EPCDEPLossAverage = EPCDEPLossTotal / (16-winCount)

	EPCOPSeasonTotal = seasonReportRaw["tEPDOP"].sum()
	EPCOPSeasonAverage = EPCOPSeasonTotal / 16
	EPCOPWinTotal = homeWins["tEPDOP"].sum() + awayWins["tEPDOP"].sum()
	EPCOPWinAverage = EPCOPWinTotal / winCount
	EPCOPLossTotal = homeLosses["tEPDOP"].sum() + awayLosses["tEPDOP"].sum()
	EPCOPLossAverage = EPCOPLossTotal / (16-winCount)

	headerRow = ['Season Total', 'Per Game', 'Win Total', 'Per Win', 'Loss Total','Per Loss']
	penaltiesRow = ['Penalties',PenaltiesSeasonTotal,PenaltiesSeasonAverage,PenaltiesWinTotal,PenaltiesWinAverage,PenaltiesLossTotal,PenaltiesLossAverage]
	EPCRow = ['EPC',EPCSeasonTotal,EPCSeasonAverage,EPCWinTotal,EPCWinAverage,EPCLossTotal,EPCLossAverage]
	EPCDHPRow = ['EPCDHP',EPCDHPSeasonTotal,EPCDHPSeasonAverage,EPCDHPWinTotal,EPCDHPWinAverage,EPCDHPLossTotal,EPCDHPLossAverage]
	EPCDEPRow = ['EPCDEP',EPCDEPSeasonTotal,EPCDEPSeasonAverage,EPCDEPWinTotal,EPCDEPWinAverage,EPCDEPLossTotal,EPCDEPLossAverage]
	EPCOPRow = ['EPCOP',EPCOPSeasonTotal,EPCOPSeasonAverage,EPCOPWinTotal,EPCOPWinAverage,EPCOPLossTotal,EPCOPLossAverage]

	fig_background_color = 'white'
	fig_border = 'black'
	data = [headerRow,penaltiesRow,EPCRow,EPCDHPRow,EPCDEPRow,EPCOPRow]

	# Pop the headers from the data array
	column_headers = data.pop(0)
	row_headers = [x.pop(0) for x in data]

	# Table data needs to be non-numeric text. Format the data
	# while I'm at it.
	cell_text = []
	for row in data:
	    cell_text.append([f'{x:1.2f}' for x in row])

	# Get some lists of color specs for row and column headers
	rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
	ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))

	# Create the figure. Setting a small pad on tight_layout
	# seems to better regulate white space. Sometimes experimenting
	# with an explicit figsize here can produce better outcome.
	plt.figure(linewidth=2,
	           edgecolor=fig_border,
	           facecolor=fig_background_color,
	           tight_layout={'pad':1},
	           figsize=(4.5,1.75)
	          )

	# Add a table at the bottom of the axes
	the_table = plt.table(cellText=cell_text,
	                      rowLabels=row_headers,
	                      rowColours=rcolors,
	                      rowLoc='right',
	                      colColours=ccolors,
	                      colLabels=column_headers,
	                      loc='center')

	# Scaling is the only influence we have over top and bottom cell padding.
	# Make the rows taller (i.e., make cell y scale larger).
	the_table.scale(1, 1.1)
	# Hide axes
	ax = plt.gca()
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	# Hide axes border
	plt.box(on=None)
	# Force the figure to update, so backends center objects correctly within the figure.
	# Without plt.draw() here, the title will center on the axes and not the figure.
	plt.draw()
	# Create image. plt.savefig ignores figure edge and face colors, so map them.
	fig = plt.gcf()
	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_penaltySummaryTable.png",
	            edgecolor=fig.get_edgecolor(),
	            facecolor=fig.get_facecolor(),
	            dpi=175
	            )
	plt.clf()

def tPEN_tEPC_graph(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

	seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

	seasonReportRaw.plot(x='Date',y=['tPEN(#)','tEPPfP'])

	plotLegend = plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)

	plotLegend.get_texts()[0].set_text('# of Penalties')
	plotLegend.get_texts()[1].set_text('EPC due to Penalties')

	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_tPENtEPPgraph.png",dpi=400,bbox_inches="tight")
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

	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_allExpPointsgraph.png",dpi=400,bbox_inches="tight")
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


	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_allPenaltiesgraph.png",dpi=400,bbox_inches="tight")
	plt.clf()

def allExpPoints_boxplot(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

	seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

	seasonReportRaw = seasonReportRaw.rename(columns={'tEPPfP':'tEPCP','tEPDHP':'tEPCDHP','tEPDEP':'tEPCDEP','tEPDOP':'tEPCOP'})

	seasonReportRaw.boxplot(column=['tEPCP','tEPCDHP','tEPCDEP','tEPCOP'])

	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_allExpPointsboxplot.png",dpi=400,bbox_inches="tight")
	plt.clf()

def allPenalties_boxplot(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

	seasonReportRaw.boxplot(column=['tPEN(#)','tDHP(#)','tDEP(#)','tOP(#)'])

	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_allPenaltiesboxplot.png",dpi=400,bbox_inches="tight")
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
	plt.savefig("Analysis/" + year + "_Wins_vs_tEPP_graph.png",dpi=400,bbox_inches="tight")
	plt.clf()

def wins_tEPCPP_graph(year):
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

			totalPens = seasonReportRaw['tPEN(#)'].sum()

			expPointsPerPen = seasonReportRaw['tEPPfP'].sum() / totalPens

			seasonInfoDict[team] = (totalwins, expPointsPerPen)

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
	y1 = gradient*x1 + intercept
	fig, ax = plt.subplots(1)
	ax.plot(x,y,'ob')
	ax.plot(x1,y1,'-r')
	fig.subplots_adjust(bottom=0.3)
	fig.text(0.1,0.15,"r-value: " + str(r_value))
	fig.text(0.1,0.1,"r-squared value: " + str(r_value**2))
	plt.savefig("Analysis/" + year + "_Wins_vs_tEPCPP_graph.png",dpi=400,bbox_inches="tight")
	plt.clf()

def wins_tPEN_graph(year):
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

			totalPens = seasonReportRaw['tPEN(#)'].sum()

			seasonInfoDict[team] = (totalwins, totalPens)

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
	y1 = gradient*x1 + intercept
	fig, ax = plt.subplots(1)
	ax.plot(x,y,'ob')
	ax.plot(x1,y1,'-r')
	fig.subplots_adjust(bottom=0.3)
	fig.text(0.1,0.15,"r-value: " + str(r_value))
	fig.text(0.1,0.1,"r-squared value: " + str(r_value**2))
	plt.savefig("Analysis/" + year + "_Wins_vs_tPEN_graph.png",dpi=400,bbox_inches="tight")
	plt.clf()

def wins_tDHP_graph(year):
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

			totalPens = seasonReportRaw['tDHP(#)'].sum()

			seasonInfoDict[team] = (totalwins, totalPens)

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
	y1 = gradient*x1 + intercept
	fig, ax = plt.subplots(1)
	ax.plot(x,y,'ob')
	ax.plot(x1,y1,'-r')
	fig.subplots_adjust(bottom=0.3)
	fig.text(0.1,0.15,"r-value: " + str(r_value))
	fig.text(0.1,0.1,"r-squared value: " + str(r_value**2))
	plt.savefig("Analysis/" + year + "_Wins_vs_tDHP_graph.png",dpi=400,bbox_inches="tight")
	plt.clf()

def wins_tDEP_graph(year):
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

			totalPens = seasonReportRaw['tDEP(#)'].sum()

			seasonInfoDict[team] = (totalwins, totalPens)

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
	y1 = gradient*x1 + intercept
	fig, ax = plt.subplots(1)
	ax.plot(x,y,'ob')
	ax.plot(x1,y1,'-r')
	fig.subplots_adjust(bottom=0.3)
	fig.text(0.1,0.15,"r-value: " + str(r_value))
	fig.text(0.1,0.1,"r-squared value: " + str(r_value**2))
	plt.savefig("Analysis/" + year + "Wins_vs_tDEP_graph.png",dpi=400,bbox_inches="tight")
	plt.clf()

def wins_tOP_graph(year):
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

			totalPens = seasonReportRaw['tOP(#)'].sum()

			seasonInfoDict[team] = (totalwins, totalPens)

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
	y1 = gradient*x1 + intercept
	fig, ax = plt.subplots(1)
	ax.plot(x,y,'ob')
	ax.plot(x1,y1,'-r')
	fig.subplots_adjust(bottom=0.3)
	fig.text(0.1,0.15,"r-value: " + str(r_value))
	fig.text(0.1,0.1,"r-squared value: " + str(r_value**2))
	plt.savefig("Analysis/" + year + "Wins_vs_tOP_graph.png",dpi=400,bbox_inches="tight")
	plt.clf()

if __name__ == '__main__':
	year = "18-19"

	wins_tEPC_graph(year)
	wins_tEPCPP_graph(year)
	wins_tPEN_graph(year)
	wins_tDHP_graph(year)
	wins_tDEP_graph(year)
	wins_tOP_graph(year)

	print("League figures created!")

	for team in teamList.teamList:
		allExpPoints_boxplot(year,team)
		allPenalties_boxplot(year,team)

		allExpPoints_graph(year,team)
		allPenalties_graph(year,team)

		tPEN_tEPC_graph(year,team)

		print(team + "'s figures created!")

	for team in teamList.teamList:
		penaltySummary_table(year,team)