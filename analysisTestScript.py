import os
import location
import teamList
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

##adapted from code from this website:
## https://towardsdatascience.com/simple-little-tables-with-matplotlib-9780ef5d0bc4

year = "18-19"

team = "ARI"

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
plt.savefig('pyplot-table-demo.png',
            edgecolor=fig.get_edgecolor(),
            facecolor=fig.get_facecolor(),
            dpi=175
            )