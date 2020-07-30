import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as numpy
from scipy import stats

seasonReportRaw = pd.read_csv("Data/19-20 ARI/ARI_SeasonRaw.csv")

seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

seasonReportRaw.boxplot(column=['tPEN(#)','tDHP(#)','tDEP(#)','tOP(#)'])

plt.savefig('test.png',dpi=400)

plt.show()