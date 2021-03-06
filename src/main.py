#!env /usr/bin/python3

import numpy as np
from math import *
from core.kmeans import KMeans
from core.spectral import SpectralClustering
from util.util import *

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Setting
number_of_iteration = 1
print_raw_data = False
number_of_clusters = 2
print_the_result = True


def parseLine(line):
    dims = line.split(',')
    return mapv(float,dims[:-1]), int(float(dims[3]))

def readData():
    inputFile = 'data/data.csv'
    with open(inputFile,'r') as fin:
        lines = fin.readlines()[1:]
    result = mapv(parseLine,lines)
    return mapv(getValue(0),result), mapv(getValue(1),result)

def parseRingDataLine(line):
    st = line[:-1].split(' ')
    result = []
    for piece in st:
        try:
            result.append(float(piece))
        except:
            pass
    return result


def readRingData():
    inputFile = 'data/ring-data.txt'
    with open(inputFile,'r')as fin:
        lines = fin.readlines()
    return mapv(parseRingDataLine,lines)

def distance(x,y):
    return sqrt((x[0]-y[0])**2
                +(x[1]-y[1])**2
                +(x[2]-y[2])**2)

def affinity(x,y):
    return np.exp(-np.square(np.linalg.norm(x-y)))

def draw3D(data,label,name = ""):
    model = partition(list(zip(data,label)),getValue(1))
    ax = plt.subplot(111,projection='3d')

    for label in model:
        position = mapv(getValue(0),model[label])
        xs = mapv(getValue(0),position)
        ys = mapv(getValue(1),position)
        zs = mapv(getValue(2),position)
        ax.scatter(xs,ys,zs)
    ax.set_title(name)
    ax.set_zlabel('Z')
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()

def draw2D(data,label,name=""):
    model = partition(list(zip(data,label)),getValue(1))
    for label in model:
        position = mapv(getValue(0),model[label])
        x = mapv(getValue(0),position)
        y = mapv(getValue(1),position)
        plt.scatter(x,y)
    plt.title(name)
    plt.show()

def printDistance(minimumd,maximumd,averaged):
    print("Minimum max distance:",minimumd)
    print("Maximum max distance:",maximumd)
    print("Average max distance:",averaged)

def testModel(data,model,distance):
    ans = {'maximum distance':9999,"labels":[]}
    maxDistance = getValue('maximum distance')
    avg,maximum_max_distance = 0,0

    for i in range(number_of_iteration):
        result = model(data,number_of_clusters,distance).solve()
        avg += maxDistance(result)
        if(maxDistance(ans) > maxDistance(result)):
            ans = result
        if(maxDistance(result) > maximum_max_distance):
            maximum_max_distance = maxDistance(result)

    avg /= number_of_iteration
    printDistance(maxDistance(ans),maximum_max_distance,avg)
    return ans['labels']

def testKMeans():
    data,label = readData()
    if print_raw_data:
        draw3D(data,label)

    labels = testModel(data,KMeans,distance)
    if print_the_result:
        draw3D(data,labels,"K-Means")

def testSpectralClustering():
    data = readRingData()
    labels = testModel(data,SpectralClustering,affinity)
    if print_the_result:
        draw2D(data,labels,"Spectral Clustring")


if __name__ == "__main__":
    testSpectralClustering()
