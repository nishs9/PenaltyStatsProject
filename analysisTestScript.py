import os
import location
import teamList
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

year="18-19"
team="ARI"

seasonReportRaw = pd.read_csv("Data/" + year + " " + team + "/" + team + "_SeasonRaw.csv")

seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

seasonReportRaw = seasonReportRaw.rename(columns={'tEPPfP':'tEPCP','tEPDHP':'tEPCDHP','tEPDEP':'tEPCDEP','tEPDOP':'tEPCOP'})

print(seasonReportRaw)

seasonReportRaw.boxplot(column=['tEPCP','tEPCDHP','tEPCDEP','tEPCOP'])

plt.savefig("Analysis/" + year + " " + team + "/" + team + "_allExpPointsboxplot.png",dpi=400)
plt.clf()