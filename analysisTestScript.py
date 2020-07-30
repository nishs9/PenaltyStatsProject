import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as numpy
from scipy import stats

seasonReportRaw = pd.read_csv("Data/19-20 ARI/ARI_SeasonRaw.csv")

seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

seasonReportRaw.plot(x="Date",y=['tPEN(#)','tEPPfP'])

plotLegend = plt.legend()

plotLegend.get_texts()[0].set_text('# of Penalties')
plotLegend.get_texts()[1].set_text('EPC due to Penalties')

plt.savefig('test.png',dpi=400)

plt.show()