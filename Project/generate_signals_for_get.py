import scipy.io
import numpy
import pandas
import pickle

matData = scipy.io.loadmat("Dataset1.mat")["Raw_Data"]
#print(matData)
fakedata = scipy.io.loadmat("fake_signal_1.mat")["data"]
print(fakedata.shape)
print(matData.shape)

dataList = []

for index,data in enumerate(matData):
    for j in data:
        tempList = []
        tempList.append(index+1)
        tempList.append(0)
        for k in j:
            tempList.append(k)
        dataList.append(tempList)

dataFrame = pandas.DataFrame(dataList)
dataFrame = dataFrame[:10]

attackMatrixData = scipy.io.loadmat("sampleAttack.mat")["attackVectors"]
fakeDataList = []

for index, data in enumerate(attackMatrixData):
    for i, d in enumerate(data):
        for j in d:
            tempList = []
            tempList.append(i+1)
            tempList.append(1)
            for k in (list(j)*4):
                tempList.append(k)
            # print(tempList)
            fakeDataList.append(tempList)

fakeDf = pandas.DataFrame(fakeDataList)

fakeDf = fakeDf[:10]

finalDF = pandas.concat([dataFrame, fakeDf], axis=0)
finalDF = finalDF.iloc[:,:482]

with open("multiple_signals.pkl", "wb") as file:
    pickle.dump(finalDF, file)

dataFrame = dataFrame.iloc[:1,:482]

with open("single_brain_signal.pkl", "wb") as file:
    pickle.dump(dataFrame, file)