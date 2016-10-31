#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
# matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math as m

from matplotlib import colors

samples = 1024

rgbBw = [[0,0,0],[1,1,1]]
rgbGbr = [[0,1,0],[0,0,1],[1,0,0]]
rgbGbrFull = [[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,0,0]]
rgbWbCustom = [[1,1,1],[1,0,1],[0,0,1],[0,1,1],[0,1,0],[1,1,0],[1,0,0],[0,0,0]]

hsvBw = [[0,0,0],[0,0,1]]
hsvGBR = [[120,1,1],[180,1,1],[240,1,1],[300,1,1],[360,1,1]]
hsvUnknown = [[120,0.5,1],[60,0.5,1],[0,0.5,1]]
hsvCustom = [[0,1,1],[120,0.9,1],[180,0.7,1],[240,0.5,1],[300,0.3,1],[310,0,1]]

def getPointInCube(listPoints,point):
    element, skala = getElement(listPoints, point)
    finalPoint = []
    for i in range(len(listPoints[element])):
        lewyZakres = listPoints[element][i]
        prawyZakres = listPoints[element + 1][i]
        div = prawyZakres - lewyZakres
        if div != 0:
            finalPoint.append(lewyZakres + (1 / (div)) * skala)
        else:
            finalPoint.append(lewyZakres)
    return finalPoint


def getElement(listPoints, point):
    element = m.trunc(point * (len(listPoints) - 1))
    if element == len(listPoints) - 1:
        element = len(listPoints) - 2
    skala = point * (len(listPoints) - 1) - element
    return element, skala


def getPointInCone(listPoints,point):
    element,skala = getElement(listPoints,point)
    finalPoint = []
    for i in range(len(listPoints[element])):
        lewyZakres = listPoints[element][i]
        prawyZakres = listPoints[element + 1][i]
        div = prawyZakres - lewyZakres
        finalPoint.append(lewyZakres + div * skala)
    return finalPoint


def plot_color_gradients(gradients, names):
    rc('legend', fontsize=10)

    column_width_pt = 400
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, samples, 3))
        for i, v in enumerate(np.linspace(0, 1, samples)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto',interpolation='none')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)
    # plt.show()
    fig.savefig('my-gradients.pdf')
    # plt.close()

def hsv2rgb(h, s, v):
    vs = v*s
    hue = h/60
    x = vs * (1 - abs((hue % 2) -1))
    switcher = {
        0: [vs,x,0],
        1: [x,vs,0],
        2: [0,vs,x],
        3: [0,x,vs],
        4: [x,0,vs],
        5: [vs,0,x]
    }
    rgb = switcher.get(m.trunc(hue),[0,0,0])
    match = v-vs
    rgb = [i+match for i in rgb]
    return rgb

def gradient_rgb_bw(v):
   return getPointInCube(rgbBw,v)

def gradient_rgb_gbr(v):
    return getPointInCube(rgbGbr,v)

def gradient_rgb_gbr_full(v):
    return getPointInCube(rgbGbrFull,v)

def gradient_rgb_wb_custom(v):
    #TODO
    return getPointInCube(rgbWbCustom,v)

def gradient_hsv_bw(v):
    hsv = getPointInCone(hsvBw,v)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])

def gradient_hsv_gbr(v):
    hsv = getPointInCone(hsvGBR,v)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])

def gradient_hsv_unknown(v):
    hsv = getPointInCone(hsvUnknown, v)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])


def gradient_hsv_custom(v):
    hsv = getPointInCone(hsvCustom, v)
    return hsv2rgb(hsv[0], hsv[1], hsv[2])

def loadMapPoints(fileName):
    with open(fileName) as file:
        mapa = file.read().splitlines()
    mapa = [i.split(' ') for i in mapa]
    mapHeight= int(mapa[0][0])
    mapWidth = int(mapa[0][1])
    distance = int(mapa[0][2])
    del mapa[0]
    for i in range(len(mapa)):
        del mapa[i][-1]
        mapa[i] = [ float(point) for point in mapa[i]]
    return mapa,mapWidth,mapHeight,distance

def createHSVmatrix(mapHeight,mapWidth):
    hsvMatrix = []
    for i in range(mapHeight):
        hsvMatrix.append([])
        for j in range(mapWidth):
            hsvMatrix[i].append([0,1,1])
    return hsvMatrix


def convertMapPoints(mapa,mapHeight,mapWidth,distance):
    minimum = np.min(mapa)
    maximum = np.max(mapa) - minimum
    sun = np.array([-7*(minimum+maximum), 7*(minimum+maximum), -7*(minimum+maximum)])
    mapaHSV = createHSVmatrix(mapHeight,mapWidth)
    matrixOfAngles = np.zeros([mapHeight,mapWidth])
    for i in range(mapHeight):
        # print([(point-minimum)/maximum for point in mapaHSV[i]])
        for j in range(mapWidth):
            mainPoint = np.array([i*distance,mapa[i][j],j*distance])
            if i % 2 == 0:
                if j < mapWidth-1:
                    secondPoint = np.array([i*distance,mapa[i][j+1],distance*(j+1)])
                    thirdPoint = np.array([(i+1)*distance,mapa[i+1][j],j*distance])
                else:
                    secondPoint = np.array([i * distance, mapa[i][j - 1], distance * (j - 1)])
                    thirdPoint = np.array([(i + 1) * distance, mapa[i + 1][j], j * distance])
            else:
                if j > 0:
                    secondPoint = np.array([i*distance,mapa[i][j-1],(j-1)*distance])
                    thirdPoint = np.array([(i-1)*distance,mapa[i-1][j],j*distance])
                else:
                    secondPoint = np.array([i * distance, mapa[i][j + 1], (j + 1) * distance])
                    thirdPoint = np.array([(i - 1) * distance, mapa[i - 1][j], j * distance])

            vectorToSun = sun - mainPoint
            normal = np.cross(secondPoint - mainPoint,thirdPoint - mainPoint)
            angleSun_Surface = m.degrees(np.arccos(np.clip(np.dot(normal,vectorToSun)/(np.linalg.norm(normal)*np.linalg.norm(vectorToSun)),-1,1)))
            matrixOfAngles[i][j] = angleSun_Surface
            mapaHSV[i][j][0] = (1-((mapa[i][j]-minimum)/maximum))*120
            if angleSun_Surface < 90.0:
                mapaHSV[i][j][1] = 1-(1-np.sin(angleSun_Surface))*1
            else:
                mapaHSV[i][j][2] = 1 - (1 - np.sin(angleSun_Surface))*5
            mapaHSV[i][j] = hsv2rgb(mapaHSV[i][j][0],mapaHSV[i][j][1],mapaHSV[i][j][2])
    # for i in range(mapHeight):
    #     for j in range(mapWidth):
    #         mapaHSV[i][j][0] = (1-((mapa[i][j]-minimum)/maximum))*120
    #
    #         if angle < 0:
    #             mapaHSV[i][j][1] = 1+angle
    #         else:
    #             mapaHSV[i][j][2] = 1-angle
    #         print(angle)
    #         mapaHSV[i][j] = hsv2rgb(mapaHSV[i][j][0],mapaHSV[i][j][1],mapaHSV[i][j][2])
    return mapaHSV

def drawMap(mapa):
    fig = plt.figure()
    plt.imshow(mapa)
    plt.show()
    fig.savefig("mapa.pdf")

if __name__ == '__main__':
    # Zadanie z gradientami
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])

    # Zadanie z mapą
    mapa,mapHeight,mapWidth,distance = loadMapPoints("big.dem")
    mapa = convertMapPoints(mapa,mapHeight,mapWidth,distance)
    drawMap(mapa)
    plt.close()
