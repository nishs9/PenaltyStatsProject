import csv
import os

team = "ARI"

folder = "19-20 " + team

directory = "C:/Users/analy/Desktop/PenaltyStatsProject/Data/2019-2020 NFL Season/" + folder

section1Header = ["Team","W","L","T","PF","PA","PD"]
section1 = [team,0,0,0,0,0,0]
section2Header = ["Date","Home Team","Home Score","Away Team","Away Score","tPEN(#)","tPEN(yards)","tDHP(#)","tDHP(yards)","tEPDHP","tDEP(#)","tDEP(yards)","tEPDEP","tOP(#)","tOP(yards)","tEPDOP"]
section2 = []
section3Header = ["tPEN(#)","tPEN(yards)","tDHP(#)","tDHP(yards)","tEPDHP","tDEP(#)","tDEP(yards)","tEPDEP","tOP(#)","tOP(yards)","tEPDOP"]
section3 = [0,0,0,0,0,0,0,0,0,0,0]
section4Header = ["Pen/G","PenYards/G","DHP/G","DHPYards/G","EPDHP/G","DEP/G","DEPYards/G","EPDEP/G","OP/G","OPYards/G","EPOP/G"]
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
                    section2[len(section2) - 1].extend(row[1:])
                    break
                else:
                    continue

print(section2[0])

section1[6] = section1[4] - section1[5]

for game in section2:
    section3[0] += int(game[5])
    section3[1] += int(game[6])
    section3[2] += int(game[7])
    section3[3] += int(game[8])
    section3[4] += float(game[9])
    section3[5] += int(game[10])
    section3[6] += int(game[11])
    section3[7] += float(game[12])
    section3[8] += int(game[13])
    section3[9] += int(game[14])
    section3[10] += float(game[15])

for stat in section3:
    avgStat = stat/16
    section4.append(avgStat)

seasonReportLoc = "C:/Users/analy/Desktop/PenaltyStatsProject/Data/2019-2020 NFL Season/" + team + "_Season.csv"

with open(seasonReportLoc, 'w', newline = '') as seasonReportFile:
    writer = csv.writer(seasonReportFile, delimiter=',')
    writer.writerow(section1Header)
    writer.writerow(section1)

    writer.writerow([])

    writer.writerow(section2Header)

    for row in section2:
        writer.writerow(row)

    writer.writerow([])

    writer.writerow(section3Header)
    writer.writerow(section3)

    writer.writerow([])

    writer.writerow(section4Header)
    writer.writerow(section4)



##print(section1)

##for line in section2:
##    print(line)

##print(section3)

##print(section4)