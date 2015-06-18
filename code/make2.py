#In this program I will use 7 of the 8 subsets of training data and calculate my own score before sending it in.
#The sets will be picked randomly. Then I will make all of the features discrete, and create a binary feature
#tree that checks entropy loss in producing predictions. This will be done twice, once for casual riders and
#once for registered.

import random
import pandas as pd
import sys
import os
import numpy as np
import make2Tree as tr

numberOfTestFiles = 8
namePathForTrainFiles = "data/train.csv"
namePathForFinalTest = "data/test.csv"
namePathForOutput = "submissions/sub3"

def main():
    testSet = random.randint(0,numberOfTestFiles)
    raw_data = getData(testSet)
    data = normalizeData(raw_data)
    features = ['hour','season','holiday','workingday','weather','atemp','humidty','windspeed']
    casual_tree = generateTree(data, "casual", features)
    reg_tree = generateTree(data, "registered", features)
    prediction = generateOutput(casual_tree, reg_tree, getTrainName(testSet))
    print score(prediction, testSet)
    prediction = generateOutput(casual_tree, reg_tree, namePathForFinalTest)
    saveOutput(prediction)


def getTrainName(num):
    path = os.path.splitext(namePathForTrainFiles)[0]
    ext = os.path.splitext(namePathForTrainFiles)[1]
    return path + str(num).zfill(3) + ext

def getData(exclude_num):
    data_ary = []
    for i in range(0,numberOfTestFiles):
	if i != exclude_num:
	    data_ary.append( pd.read_csv(getTrainName(i)) )
    return pd.concat(data_ary)

def normalizeData(rawDF):
    cols = ['temp','atemp','humidity','windspeed']
    for col in cols:
	rawDF[col] = pd.qcut(rawDF[col],[0,.25,.5,.75,1],labels=[0,1,2,3])
    return rawDF

def generateTree(data, treeType, features):
    if len(features) == 0:
	return tr.make2Tree(True,np.mean(data[treeType]))

    lowestStdDev = np.std(data[treeType])
    bestFeature = "nothing"

    for feature in features:
	for values in range(data[feature]):
	    
    
    
    
    



    



if __name__ == "__main__": main()
