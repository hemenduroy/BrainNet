import pandas
import scipy.io
import numpy
import pickle

matData = scipy.io.loadmat("Dataset1.mat")["Raw_Data"]
#print(matData)

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
dataFrame.rename(columns = { 0: "People", 1: "Class"}, inplace=True)

print(dataFrame)

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
fakeDf.rename(columns= {0:'People',1:'Class'}, inplace = True)
print(fakeDf)

finalDF = pandas.concat([dataFrame, fakeDf], axis=0)
finalDF = finalDF.iloc[:,:482]
print(finalDF)

with open("brain_singals_df.pkl", "wb") as file:
    pickle.dump(finalDF, file)