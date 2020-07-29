import pandas as pd
import csv
import matplotlib.pyplot as plt

seasonReportRaw = pd.read_csv("Data/19-20 ARI/ARI_SeasonRaw.csv")

seasonReportRaw['Date'] = seasonReportRaw['Date'].astype('datetime64[ns]')

print(seasonReportRaw.plot(x='Date',y=['tPEN(#)','tDHP(#)']))

plt.show()