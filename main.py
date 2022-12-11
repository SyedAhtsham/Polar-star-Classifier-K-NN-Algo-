
# Dataset Info

# 1. Mean of the integrated profile.
# 2. Standard deviation of the integrated profile.
# 3. Excess kurtosis of the integrated profile.
# 4. Skewness of the integrated profile.
# 5. Mean of the DM-SNR curve.
# 6. Standard deviation of the DM-SNR curve.
# 7. Excess kurtosis of the DM-SNR curve.
# 8. Skewness of the DM-SNR curve.
# 9. Class
#
# HTRU 2 Summary
# 17,898 total examples.
# 1,639 positive examples.
# 16,259 negative examples.


import copy
import math

K = 27

def getMinimum(dataset):

    min = []

    for i in range(8):
        if i == 2 or i == 3:
            continue
        min.append(dataset[0][i])

    myList = []

    for data in dataset:
        if data[0] < min[0]:
            min[0] = data[0]
        if min[1] > data[1]:
            min[1] = data[1]
        if min[2] > data[4]:
            min[2] = data[4]
        if min[3] > data[5]:
            min[3] = data[5]
        if min[4] > data[6]:
            min[4] = data[6]
        if min[5] > data[7]:
            min[5] = data[7]

    return min




def getMaximum(dataset):

    max = []

    for i in range(8):
        if i == 2 or i == 3:
            continue
        max.append(dataset[0][i])


    for data in dataset:
        if data[0] > max[0]:
            max[0] = data[0]
        if max[1] < data[1]:
            max[1] = data[1]
        if max[2] < data[4]:
            max[2] = data[4]
        if max[3] < data[5]:
            max[3] = data[5]
        if max[4] < data[6]:
            max[4] = data[6]
        if max[5] < data[7]:
            max[5] = data[7]

    return max



def normalize(dataset):

    maxMinusMin = []

    min = getMinimum(dataset)
    max = getMaximum(dataset)

    for (item1, item2) in zip(min, max):
        maxMinusMin.append(item2-item1)


    for data in dataset:
        data[0] = (data[0] - min[0]) / maxMinusMin[0]
        data[1] = (data[1] - min[1]) / maxMinusMin[1]
        data[4] = (data[4] - min[2]) / maxMinusMin[2]
        data[5] = (data[5] - min[3]) / maxMinusMin[3]
        data[6] = (data[6] - min[4]) / maxMinusMin[4]
        data[7] = (data[7] - min[5]) / maxMinusMin[5]




def euclideanDist(dataset, testDataset):
    global K
    euclideanDistances = list()
    for testData in testDataset:
        for data in dataset:
            tempED = 0
            for i in range(8):
                tempED += math.pow((data[i]-testData[i]), 2)
            tempED = math.sqrt(tempED)

            euclideanDistances.append([tempED, data[8]])

        euclideanDistances.sort()
        countPositives = 0
        for m in range(K):
            if euclideanDistances[m][1] == 1:
                countPositives += 1

        if countPositives > (K/2):
            testData[8] = 1
        else:
            testData[8] = 0


        euclideanDistances.clear()


def manhattanDist(dataset, testDataset):
    global K
    manhattanDistances = list()
    for testData in testDataset:
        for data in dataset:
            tempMD = 0
            for i in range(8):
                tempMD += abs(data[i]-testData[i])

            manhattanDistances.append([tempMD, data[8]])

        manhattanDistances.sort()
        countPositives = 0
        for m in range(K):
            if manhattanDistances[m][1] == 1:
                countPositives += 1

        if countPositives > (K/2):
            testData[8] = 1
        else:
            testData[8] = 0


        manhattanDistances.clear()



def infinityNorm(dataset, testDataset):
    global K
    infinityNormDistances = list()
    for testData in testDataset:
        for data in dataset:
            tempIN = list()
            for i in range(8):
                tempIN.append(abs(data[i]-testData[i]))

            tempIN.sort(reverse=True)
            infinityNormDistances.append([tempIN[0], data[8]])

        infinityNormDistances.sort()
        countPositives = 0
        for m in range(K):
            if infinityNormDistances[m][1] == 1:
                countPositives += 1

        if countPositives > (K/2):
            testData[8] = 1
        else:
            testData[8] = 0


        infinityNormDistances.clear()



def cosineSimilarity(dataset, testDataset):
    global K
    cosineSimilarityMeasures = list()
    for testData in testDataset:
        for data in dataset:
            nominator = 0
            denominator = 0
            dataNorm = 0
            testDataNorm = 0
            for i in range(8):
                nominator += (testData[i]*data[i])
                dataNorm += math.pow(data[i], 2)
                testDataNorm += math.pow(testData[i], 2)

            denominator = math.sqrt(dataNorm)*math.sqrt(testDataNorm)
            cosineSim = nominator/denominator

            cosineSimilarityMeasures.append([cosineSim, data[8]])

        cosineSimilarityMeasures.sort(reverse=True)
        countPositives = 0
        for m in range(K):
            if cosineSimilarityMeasures[m][1] == 1:
                countPositives += 1

        if countPositives > (K/2):
            testData[8] = 1
        else:
            testData[8] = 0


        cosineSimilarityMeasures.clear()


def intersectionSimilarity(dataset, testDataset):
    global K
    intersectionSimilarityMeasures = list()
    for testData in testDataset:
        for data in dataset:
            nominator = 0
            denominator = 0
            intersectionSim = 0
            for i in range(8):

                nominator = min(data[i], testData[i])
                denominator = max(data[i], testData[i])
                result = nominator/denominator
                intersectionSim += result

            intersectionSimilarityMeasures.append([intersectionSim, data[8]])

        intersectionSimilarityMeasures.sort(reverse=True)
        countPositives = 0
        for m in range(K):
            if intersectionSimilarityMeasures[m][1] == 1:
                countPositives += 1

        if countPositives > (K/2):
            testData[8] = 1
        else:
            testData[8] = 0


        intersectionSimilarityMeasures.clear()



def computerAccuracy(classifiedByModel, testingData):
    n = len(testingData)

    correctPreds = 0
    for (data1, data2) in zip(classifiedByModel, testingData):
        if data1[8] == data2[8]:
            correctPreds += 1

    return (correctPreds/n)





# Opening the dataset file for reading the data

datasetFile = open("HTRU_2.csv", "r")

attributesData = list()

trainingSetPercent = 0
testingSetPercent = 0

# reading data from the csv line by line and seperating the attributes using split function
n = 0
for line in datasetFile:
    data = line.strip("\n").split(",")
    attributesData.append(data)
    n += 1


attributesData = [[float(float(j)) for j in i] for i in attributesData]

normalize(attributesData)


# total Number of instances in the dataset
N = n

# training set will be 80 percent of the total number of instanes N
trainingSetPercent = round(0.8 * N)
# testing set will be 20 percent of the total number of instanes N
testingSetPercent = round(0.2 * N)

# print(trainingSetPercent)
# print(testingSetPercent)
#
# print(trainingSetPercent+testingSetPercent)

trainingSet = list()
testingSet = list()


# dividing and storing the instances in trainingSet and testingSet
i = 0
for item in attributesData:
    if i < trainingSetPercent:
        trainingSet.append(item)
    else:
        testingSet.append(item)

    i += 1








classifiedByModel = copy.deepcopy(testingSet)

euclideanDist(trainingSet, classifiedByModel)

# manhattanDist(trainingSet, classifiedByModel)

#
# for data in classifiedByModel:
#     if data[8] == 1:
#         print(data)

# infinityNorm(trainingSet, classifiedByModel)

# cosineSimilarity(trainingSet, classifiedByModel)

# intersectionSimilarity(trainingSet, classifiedByModel)

# for item in testingSet:
#     if item[8] == 1:
#         print(item)

# print("ClassifiedByModel:")
# for data in classifiedByModel:
#     if data[8] == 1:
#         print(data)


accuracy = computerAccuracy(classifiedByModel, testingSet)

print("Percentage Accuracy of Model at K="+str(K) +" : " + str(round(accuracy*100, 2)))