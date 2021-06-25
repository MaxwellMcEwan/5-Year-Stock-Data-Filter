# PYTHON EXTRA CREDIT
# Maxwell McEwan
# This was a project of mine I did a few days ago. I'm making a stock trading game and wanted it to use historical stock data. I pulled historical data off of the internet and they were in CSV's. They had info I didn't really want either. I've gotten a lot better at files and sorting through data this year in python so I just did it in python then imported it over to my Unity project (It feels a lot easier for me to do the heavy lifting in python than in C#).

# import our CSV module
import csv
import os
import glob

# These are the rows of the CSV file we want it inclues stock opens, closes, highs and lows for 2459 trading days my game uses linear interpolation between the four points with a bit of randomization in between.
wantedNums = [1, 3, 4, 5]

allChosen = []

currentRow = 0

PREVIOUS_STOCK_VALUES = glob.glob("C:/Users/Vanil/PycharmProjects/RefiningStockData/STOCK_VALUES/*")
PREVIOUS_STOCK_INFO = glob.glob("C:/Users/Vanil/PycharmProjects/RefiningStockData/STOCK_ALL_INFO/*")

for value in PREVIOUS_STOCK_VALUES:
    os.remove(value)

for info in PREVIOUS_STOCK_INFO:
    os.remove(info)

with open("NASDAQ_SCREENER.csv") as ALL_SCREEN_DATA:
    SCREEN_READER = csv.reader(ALL_SCREEN_DATA, delimiter=',', quotechar=' ')
    for row in SCREEN_READER:
        if currentRow != 0:
            if row[7] != "" and int(row[7]) < 2015:
                allChosen.append(row[0] + "," + row[1])
        currentRow += 1

# Ya that's pretty much it. I wanted the process to filter more data to be easy so all I have to do it drag in the new CSV file and write the companies name in the stock data list. It would be cool if I could use requests to pull the file from the website automatically. I may do that down the road but just for getting the game started I don't really need a ton of data!

# TESTING FOR AUTOMATIC DOWNLOADS WITH ONLY TYPING IN THE NAME OF THE STOCK.
import requests
import progressbar
from pathlib import Path

progressbar.streams.wrap_stderr()

bar = progressbar.ProgressBar(max_value=len(allChosen))

for i in range(len(allChosen)-1):
    choseParts = allChosen[i].split(",")

    requests.session().cookies.clear()

    downloadedData = requests.get("https://query1.finance.yahoo.com/v7/finance/download/" + choseParts[
        0] + "?period1=1466121600&period2=1623888000&interval=1d&events=history&includeAdjustedClose=true.csv",
                                  allow_redirects=True)

    open(choseParts[0] + '.csv', 'wb').write(downloadedData.content)
    Path("C:/Users/Vanil/PycharmProjects/RefiningStockData/" + choseParts[0] + ".csv").rename(
        "C:/Users/Vanil/PycharmProjects/RefiningStockData/STOCK_ALL_INFO/" + choseParts[0] + ".csv")

    with open("STOCK_ALL_INFO/"+choseParts[0] + '.csv', 'r') as newData:
        newDataReader = csv.reader(newData, delimiter=',', quotechar=' ')
        dataList = list(newDataReader)
        allDataToWrite = []
        ranReader = False

        if dataList[0][0][0] == "4":
            allChosen.remove(allChosen[i])
            os.remove("C:/Users/Vanil/PycharmProjects/RefiningStockData/STOCK_ALL_INFO/" + choseParts[0] + ".csv")
        else:
            ranReader = True
            for row in newDataReader:
                if row[0] != "Date":
                    dataToWrite = ""
                    for item in range(1, 5):
                        dataToWrite += row[item] + " "
                    dataToWrite += "\n"
                    allDataToWrite.append(dataToWrite)

            newTextData = open(choseParts[0] + '.txt', 'w').writelines(allDataToWrite)

        if ranReader:
            Path("C:/Users/Vanil/PycharmProjects/RefiningStockData/" + choseParts[0] + ".txt").rename("C:/Users/Vanil/PycharmProjects/RefiningStockData/STOCK_VALUES/" + choseParts[0] + ".txt")

    bar.update(i)
