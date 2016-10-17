#!/usr/bin/env python
# -*- coding utf-8 -*-
import matplotlib.pyplot as plt

def generation(column,cell,krotka):
    krotka[2] = float(cell)

def effort(column,cell,krotka):
    krotka[0] = float(cell)

def run(column,cell,krotka):
    krotka[1].append(float(cell))

def checkCell(column,cell,krotka):
    # print(column)
    switcher = {
        "generation": generation,
        "effort": effort,
    }
    function = switcher.get(column,run)
    function(column,cell,krotka)

def warunki(krotka):
    if krotka[0] > 500000:
        return False
    elif krotka[2] > 199:
        return False
    return True

def readFile(fileName):
    readFile = open(fileName,"r")
    lines = readFile.readlines();
    readFile.close();
    plotArray = [[]]*3
    for i in range(len(plotArray)):
        plotArray[i] = [None]
    # print(plotArray)
    for i in range(len(lines)):
        if i == 0:
            # print("test")
            columns = lines[i]
            columns = columns.split(",")
        else:
            cells = lines[i].split(',')
            krotka = [0,[],0]
            for j in range(len(cells)):
                # print(cells)
                checkCell(columns[j],cells[j],krotka);
            krotka[1] = sum(krotka[1])/len(krotka[1])
            if warunki(krotka) == True:
                plotArray[0].append(krotka[0])
                plotArray[1].append(krotka[1])
                plotArray[2].append(krotka[2])
            else:
                print("Warunek nie spełniony")
    # print(len(plotArray[0]))
    # print(len(plotArray[1]))
    # print(len(plotArray[2]))
    return plotArray


def readAllFiles(fileList):
    plotList = []
    for name in fileList:
        plotList.append(readFile(name))
    return plotList


def addColorsToPlots(colors,plotList):
    for i in range(len(plotList)):
        plotList[i].append(colors[i])
    return plotList

def drawLinePlot(plotList):
    axis1 = plt.subplot(121)
    for newPlot in plotList:
        axis1.plot(newPlot[0],newPlot[1],newPlot[3])
    plt.savefig('wykresy.png')
    plt.close()

def main():
    fileList = ["cel.csv","cel-rs.csv","2cel.csv","2cel-rs.csv","rsel.csv"]
    plotColors = ["k","g","m","r","b"]

    newPlotList = readAllFiles(fileList)
    newPlotList = addColorsToPlots(plotColors,newPlotList)
    drawLinePlot(newPlotList)


if __name__ == '__main__':
    main()
