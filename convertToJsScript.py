import csv
import os
import teamList

seasonReportCsvLoc = 'C:/Users/snish/Desktop/PenaltyStatsProject/Data/18-19 ARI/ARI_SeasonWeb.csv'
seasonReportTxtLoc = 'C:/Users/snish/Desktop/PenaltyStatsWebsite/nextjs-blog/public/data/ARI_SeasonWebJS.txt'

with open(seasonReportTxtLoc, 'w') as seasonReportTxt:
    seasonReportTxt.write("const text = `")
    with open(seasonReportCsvLoc, 'r') as seasonReportCsv:
        for row in csv.reader(seasonReportCsv):
            seasonReportTxt.write(",".join(row) + '\n')
    seasonReportTxt.write("`;")
    seasonReportTxt.write("\n")
    seasonReportTxt.write("\n")
    seasonReportTxt.write("export default text;")

    pre, ext = os.path.splitext(seasonReportTxtLoc)

os.rename(seasonReportTxtLoc, pre + ".js")

