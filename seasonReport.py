import csv
import os

team = "ATL"

folder = "19-20 " + team

directory = "C:/Users/analy/Desktop/PenaltyStatsProject/Data/2019-2020 NFL Season/" + folder

section1Header = []
section1 = [team,0,0,0,0,0,0]
section2Header = []
section2 = []
section3Header = []
section3 = [0,0,0,0,0,0,0,0,0,0,0]
section4Header = []
section4 = []

for filename in os.listdir(directory):
    csvLoc = directory + "/" +filename 
    with open(csvLoc) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        onPenAgg = False

        for row in csv_reader:
            ##print(row)
            if line_count == 0:
                line_count += 1
                continue

            if line_count == 1:
                section2.append(row)
                line_count += 1

                if row[1] == team:
                    if int(row[2]) > int(row[4]):
                        section1[1] += 1
                    elif int(row[2]) == int(row[4]):
                        section1[3] += 1
                    else:
                        section1[2] += 1
                    section1[4] += int(row[2])
                    section1[5] += int(row[4])
                else:
                    if int(row[2]) < int(row[4]):
                        section1[1] += 1
                    elif int(row[2]) == int(row[4]):
                        section1[3] += 1
                    else:
                        section1[2] += 1
                    section1[4] += int(row[4])
                    section1[5] += int(row[2])

                continue

            if row == ['Team', 'tPEN(#)', 'tPEN(yards)', 'tDHP(#)', 'tDHP(yards)', 'tEPDHP', 'tDEP(#)', 'tDEP(yards)', 'tEPDEP', 'tOP(#)', 'tOP(yards)', 'tEPOP']:
                onPenAgg = True

            if onPenAgg == True:
                if row[0] == team:
                    section2[len(section2) - 1].extend(row)
                    break
                else:
                    continue

for game in section2:
    section3[0] += int(game[6])
    section3[1] += int(game[7])
    section3[2] += int(game[8])
    section3[3] += int(game[9])
    section3[4] += float(game[10])
    section3[5] += int(game[11])
    section3[6] += int(game[12])
    section3[7] += float(game[13])
    section3[8] += int(game[14])
    section3[9] += int(game[15])
    section3[10] += float(game[16])

for stat in section3:
    avgStat = stat/16
    section4.append(avgStat)

seasonReportLoc = directory + "/" + folder + " Season.csv"

with open(seasonReportLoc, 'w', newLine = '') as seasonReportFile:
    writer = csv.writer(seasonReportFile, delimiter=',')



print(section1)

for line in section2:
    print(line)

print(section3)

print(section4)