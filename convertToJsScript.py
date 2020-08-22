import csv
import os
import teamList

years = ["18-19", "19-20"]

for year in years:
    for team in teamList.teamList:
        folder = year + " " + team
        seasonReportCsvLoc = 'C:/Users/snish/Desktop/PenaltyStatsProject/Data/' + folder + '/' + team + '_SeasonWeb.csv'
        seasonReportTxtLoc = 'C:/Users/snish/Desktop/PenaltyStatsWebsite/nextjs-blog/public/data/' + year + team + '_SeasonWebJS.txt'

        with open(seasonReportTxtLoc, 'w') as seasonReportTxt:
            seasonReportTxt.write("const text = `")
            with open(seasonReportCsvLoc, 'r') as seasonReportCsv:
                for row in csv.reader(seasonReportCsv):
                    seasonReportTxt.write(",".join(row) + '\n')
            seasonReportTxt.write("`;")
            seasonReportTxt.write("\n")
            seasonReportTxt.write("\n")
            seasonReportTxt.write("module.exports = {csv:function(){return text;}}")

            pre, ext = os.path.splitext(seasonReportTxtLoc)

        os.rename(seasonReportTxtLoc, pre + ".js")

