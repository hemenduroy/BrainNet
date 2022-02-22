from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from extract_features import petrosian_fractal_dimensions, hurst, zero_crossing, fft_beta, discrete_Wavelet_Transform
from sklearn.preprocessing import StandardScaler  
import pickle
import time

## ADD FUNCTIONS TO TEST DATA COMING FROM THE PHONE USING PREVIOUSLY TRAINED MODELS
def prediction(dataFrameData):
    slicedDataFrameData = dataFrameData.iloc[:,:482]
    modelFiles = ["ada_model.pkl", "svm_model_trained_1.pkl", "lr_model.pkl", "rf_model.pkl", "HC_Model.pkl", "mlpc_model_trained_1.pkl"]
    modelFileToModelMapper = {
        "ada_model.pkl" : "ADA BOOSTING",
        "svm_model_trained_1.pkl" : "SUPPORT VECTOR MACHINE",
        "rf_model.pkl" : "RANDOM FOREST CLASSIFIER",
        "lr_model.pkl" : "LOGISTIC REGRESSION",
        "HC_Model.pkl" : "HIERARCHICAL CLUSTERING",
        'mlpc_model_trained_1.pkl' : "MULTILAYER PERCEPTRON CLASSIFIER"
    }
    size = len(slicedDataFrameData)
    print(size)

    features = slicedDataFrameData.iloc[:,:2]
    data = slicedDataFrameData.iloc[:,2:]

    features["Hurst"] = data.apply(lambda line: hurst(line), axis = 1)
    features[['crossing','rate']]= data.apply(lambda line: zero_crossing(line), axis = 1, result_type = 'expand')
    features['FFT_beta']= data.apply(lambda line: fft_beta(line), axis = 1)
    features[['VAR', 'SKEW', 'KURTOSIS']]= data.apply(lambda line: discrete_Wavelet_Transform(line), axis = 1, result_type = 'expand')
    features["PFD"] = data.apply(lambda line: petrosian_fractal_dimensions(line), axis = 1)

    features = features.dropna()
    x_test = features.loc[:, 'Hurst' : 'PFD']
    y_test = features.iloc[:,1]
    
    if(size >1):
        
        ## TEST AGAINST DATA RECIEVED FROM MOBILE
        maxAccuracyScore = -1
        returnedFalseAcceptRate = -1
        returnedFalseRejectRate = -1
        returnedHalfTotalError = -1
        returnedF1Score = -1
        machineLearningAlgorithm = ""
        for filename in modelFiles:
            begin = time.time()
            modelFile = open(filename, "rb")
            model = pickle.load(modelFile)
            modelFile.close()
            if(filename == "svm_model_trained_1.pkl" or filename == "lr_model.pkl" or filename == "HC_Model.pkl"):
                stdsc = StandardScaler()
                trainedDataFile = open('train_data.pkl', "rb")
                trainedData = pickle.load(trainedDataFile)
                trainedDataFile.close() 
                stdsc.fit_transform(trainedData)           
                test_data = stdsc.transform(x_test)
            else:
                test_data = x_test
            if(filename == "HC_Model.pkl"):
                print("Here")
                y_pred = model.fit_predict(test_data)
            else:
                print("Not here")
                y_pred = model.predict(test_data)
            print("*"*50)
            print(modelFileToModelMapper[filename])
            print("Execution Time : " ,(time.time() - begin),"s")
            falseAcceptRate, falseRejectRate, halfTotalError, f1Score, accuracyScore = ml_metrics(y_test, y_pred)
            if (accuracyScore > maxAccuracyScore):
                machineLearningAlgorithm = modelFileToModelMapper[filename]
                maxAccuracyScore = accuracyScore
                returnedFalseAcceptRate = falseAcceptRate
                returnedFalseRejectRate = falseRejectRate
                returnedHalfTotalError = halfTotalError
                returnedF1Score = f1Score
        return returnedFalseAcceptRate, returnedFalseRejectRate, returnedHalfTotalError, returnedF1Score, maxAccuracyScore, machineLearningAlgorithm,-1
    
    else :
        ## TEST AGAINST DATA RECIEVED FROM MOBILE
        count = [0,0]
        for filename in modelFiles:
            if(filename == "HC_Model.pkl"):
                continue
            begin = time.time()
            modelFile = open(filename, "rb")
            model = pickle.load(modelFile)
            modelFile.close()
            if(filename == "svm_model_trained_1.pkl" or filename == "lr_model.pkl"):
                stdsc = StandardScaler()
                trainedDataFile = open('train_data.pkl', "rb")
                trainedData = pickle.load(trainedDataFile)
                trainedDataFile.close() 
                stdsc.fit_transform(trainedData)           
                test_data = stdsc.transform(x_test)
            else:
                test_data = x_test
            if(filename == "HC_Model.pkl"):
                y_pred = model.fit_predict(test_data)
            else:
                y_pred = model.predict(test_data)
            print("*"*50)
            print(modelFileToModelMapper[filename])
            print("Execution Time : " ,(time.time() - begin))
            print("CLASS : ", y_pred[0])
            if(int(y_pred[0] == 0)):
                count[0]+=1
            else:
                count[1]+=1
        liveness = 0
        if(count[1] > count[0]):
            liveness = 1
        return -1,-1,-1,-1,-1,"",liveness
    
def ml_metrics(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    truePositive,falsePositive,falseNegative,trueNegative = cm[0][0],cm[0][1],cm[1][0], cm[1][1]
    falseAcceptRate = round((falsePositive)/(falsePositive+trueNegative),3)
    falseRejectRate = round((falseNegative)/(truePositive+falseNegative),3)
    halfTotalError = round((falseAcceptRate + falseRejectRate)/2,3)
    f1Score = round((f1_score(y_test,y_pred)))
    accuracyScore = accuracy_score(y_test, y_pred)
    print("False Accept Rate : ", falseAcceptRate)
    print("False Reject Rate : ", falseRejectRate)
    print("Half Total Error : ", halfTotalError)
    print("F1 Score : ", f1Score)
    print("Accuracy : ", round(accuracyScore,4)*100,"%")
    return falseAcceptRate, falseRejectRate, halfTotalError, f1Score, accuracyScore