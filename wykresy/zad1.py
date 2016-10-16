#!/usr/bin/env python
# -*- coding utf-8 -*-
import matplotlib.pyplot as plt

def generation(column,cell,array):
    if array[2][0] == None:
        array[2][0] = float(cell)
    else:
        array[2].append(float(cell))

def effort(column,cell,array):
    if array[0][0] == None:
        array[0][0] = float(cell)
    else:
        array[0].append(float(cell))

def run(column,cell,array):
    if array[1][0] == None:
        array[1][0] = [float(cell)]
    else:
        if len(array[1]) < len(array[0]):
            array[1].append([float(cell)])
        else:
            array[1][len(array[1])-1].append(float(cell))

def checkCell(column,cell,array):
    # print(column)
    switcher = {
        "generation": generation,
        "effort": effort,
    }
    function = switcher.get(column,run)
    function(column,cell,array)

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
    plotArray = [0] * 3;
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
            for j in range(len(cells)):
                # print(cells)
                checkCell(columns[j],cells[j],plotArray);
            plotArray[1][-1] = sum(plotArray[1][-1])/len(plotArray[1][-1])
            krotka = [plotArray[0][-1],plotArray[1][-1],plotArray[2][-1]]
            if warunki(krotka) == False:
                print("Warunek nie spelniony")
                for d in range(3):
                    del plotArray[d][-1]
    # print(len(plotArray[0]))
    # print(len(plotArray[1]))
    # print(len(plotArray[2]))
    return plotArray


def readAllFiles(fileList):
    plotList = []
    for name in fileList:
        plotList.append(readFile(name))
    return plotList

def drawLinePlot(plotList):
    for newPlot in plotList:
        plt.plot(newPlot[0],newPlot[1],newPlot[3])
    plt.savefig('test.png')
    plt.close()

def addColorsToPlots(colors,plotList):
    for i in range(len(plotList)):
        plotList[i].append(colors[i])
    return plotList

def main():
    fileList = ["cel.csv","cel-rs.csv","2cel.csv","2cel-rs.csv","rsel.csv"]
    plotColors = ["k","g","m","r","b"]

    newPlotList = readAllFiles(fileList)
    newPlotList = addColorsToPlots(plotColors,newPlotList)
    drawLinePlot(newPlotList)


if __name__ == '__main__':
    main()
