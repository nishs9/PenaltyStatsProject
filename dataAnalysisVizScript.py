import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as numpy
from scipy import stats

year = "19-20"
team = "ARI"

def tPEN_tEPP_graph(year,team):
	seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

	seasonReportRaw['Date'] = seasonReportRaw['Date'].asType('datetime64[ns]')

	seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

	seasonReportRaw.plot(x='Date',y=['tPEN(#)','tEPPfP'])

	plotLegend = plt.legend()

	plotLegend.get_texts()[0].set_text('# of Penalties')
	plotLegend.get_texts()[1].set_text('EPC due to Penalties')

	plt.savefig("Data/" + year + " " + team + "/" + team + "_tPENtEPPgraph.png",dpi=400)

if __name__ == '__main__':