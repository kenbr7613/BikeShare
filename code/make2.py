#In this program I will use 7 of the 8 subsets of training data and calculate my own score before sending it in.
#The sets will be picked randomly. Then I will make all of the features discrete, and create a binary feature
#tree that checks standard deviation reduction in producing predictions. This will be done twice, once for 
#casual riders and once for registered.

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
stdRange = 2

def main():

    os.chdir(os.pardir)

    #One of the sets will be exluded from the learn set and used for test
    testSet = random.randint(0,numberOfTestFiles)
    #read in the data, excluding the test set
    print "Reading Data..."
    raw_data = getData(testSet)
    #make the continous values discrete 0-3
    print "Cleaning Data..."
    data = normalizeData(raw_data)
    features = ['hour','season','holiday','workingday','weather','atemp','humidity','windspeed']
    print "Building tree for Casual riders..."
    casual_tree = generateTree(data, "casual", features)
    print "Building tree for Registered riders..."
    reg_tree = generateTree(data, "registered", features)
    print "Generating prediciton"
    prediction = generateOutput(casual_tree, reg_tree, getTrainName(testSet))
    print score(prediction, getTrainName(testSet))
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

    rawDF['datetime'] = rawDF.convert_objects(convert_dates='coerce')
    rawDF['hour'] = rawDF['datetime'].map(lambda x: x.hour)

    return rawDF

def generateTree(data, treeType, features):

    startingStd = np.std(data[treeType])
    lowestStdDev = startingStd
    bestFeature = "nothing"
    bestFeatureVal = -1

    for feature in features:
	for value in range(data[feature].min(), data[feature].max()):
	    data1 = data.loc[data[feature] == value]
	    data2 = data.loc[data[feature] != value]
	    #SDR = standard deviation reduction
	    SDR = len(data1) * np.std(data1[treeType]) + len(data2) * np.std(data2[treeType])
	    SDR = SDR / len(data)
	    if SDR < lowestStdDev:
		lowestStdDev = SDR
		bestFeature = feature
		bestFeatureVal = value

	#reduction is actually calculated down here
    if (bestFeature == "nothing") or ((startingStd - lowestStdDev) < stdRange):
	return tr.make2Tree(True,[np.mean(data[treeType])])
    else:
	newTree = tr.make2Tree(False, [bestFeatureVal, bestFeature])
        data1 = data.loc[data[bestFeature] == bestFeatureVal]
	data2 = data.loc[data[bestFeature] != bestFeatureVal]
	newTree.insertLeft(generateTree(data1, treeType, features))
	newTree.insertRight(generateTree(data2, treeType, features))
	return newTree


def generateOutput(casual_tree, reg_tree, setPath):

    data = pd.read_csv(setPath)
    data = normalizeData(data)

    toReturn = pd.DataFrame(columns = ['datetime','count'])

    print 'Date\tPrediction\tActual\n'
    for index, row in data.iterrows():
	cCount = predictCount(casual_tree, row)
	rCount = predictCount(reg_tree, row)
	totalCount = cCount + rCount
	print row['datetime'],
	print "\t" + str(totalCount),
	print "\t" + str(row['count'])
	toReturn.loc[len(toReturn)] = [ row['datetime'] , totalCount]

    return toReturn

def predictCount(tree, row):
    while(not(tree.getIsLeaf())):
	if(row[tree.getFeature()] == tree.getVal()):
	    tree = tree.getLeft()
	else:
	    tree = tree.getRight()

    return tree.getVal()


def score(predictionDF, answerPath):
    print len(predictionDF)
    ans = pd.read_csv(answerPath)
    ans['datetime'] = ans.convert_objects(convert_dates='coerce')
    print len(ans)
    data = pd.DataFrame.merge(predictionDF, ans, left_on='datetime', right_on='datetime', how='inner')
    print len(data)
    total = 0
    for index, row in data.iterrows():
	print "test"
	total = total + np.sqaure(np.log(row['count_x'] + 1) - log(row['count_y']+1))
    print total 
    score =  np.sqrt(total / len(data)) + "\n"
    return score
	
	

def saveOutput(predictionStr): 
    return
    
    



    



if __name__ == "__main__": main()
