import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as numpy
from scipy import stats

def tPEN_tEPP_graph(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

	seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

	seasonReportRaw.plot(x='Date',y=['tPEN(#)','tEPPfP'])

	plotLegend = plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)

	plotLegend.get_texts()[0].set_text('# of Penalties')
	plotLegend.get_texts()[1].set_text('EPC due to Penalties')

	plt.savefig("Analysis/" + year + " " + team + "/" + team + "_tPENtEPPgraph.png",dpi=400)

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


if __name__ == '__main__':
	year = "19-20"
	team = "ARI"

	tPEN_tEPP_graph(year,team)
	allExpPoints_graph(year,team)
	allPenalties_graph(year,team)