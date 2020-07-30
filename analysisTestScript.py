import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as numpy
from scipy import stats

seasonReportRaw = pd.read_csv("Data/19-20 ARI/ARI_SeasonRaw.csv")

seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

seasonReportRaw['tEPPfP'] = seasonReportRaw['tEPDHP'] + seasonReportRaw['tEPDEP'] + seasonReportRaw['tEPDOP']

seasonReportRaw.plot(x="Date",y=['tEPPfP','tEPDHP','tEPDEP','tEPDOP'])

plotLegend = plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)

plotLegend.get_texts()[0].set_text('EPC due to Penalties')
plotLegend.get_texts()[1].set_text('EPC due to DHPs')
plotLegend.get_texts()[2].set_text('EPC due to DEPs')
plotLegend.get_texts()[3].set_text('EPC due to OPs')


plt.savefig('test.png',dpi=400)

plt.show()