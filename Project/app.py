from flask import Flask, request,redirect
import pandas
import pickle
import json
from prediction import prediction

filename = "multiple_signals.pkl"
#filename = "single_brain_signal.pkl"
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/get-brain-signals")
def recieve_brain_signals():
    dataFile = open(filename, "rb")
    dataFrame = pickle.load(dataFile)
    print(dataFrame)
    dataFile.close()
    jsonData = json.loads(dataFrame.to_json(orient="records"))
    return {"status" : 200, "brain_signals" : jsonData}

@app.route("/classify-brain-signals", methods=["POST"])
def classify_brain_signals():
    data = request.get_json()
    data = data["nameValuePairs"]["brain_signals"]["values"]
    list = []
    for brain_data in data:
        list.append(brain_data["nameValuePairs"])

    dataFrame = pandas.json_normalize(list)
    falseAcceptRate, falseRejectRate, halfTotalError, f1Score, accuracyScore, machineLearningAlgorithm, liveness = prediction(dataFrame)
    
    returnObj =  {
        "machine_learning_algorithm" : machineLearningAlgorithm,
        "status" : 200, 
        "accuracy_score" : accuracyScore,
        "false_accept_rate" : falseAcceptRate,
        "fale_reject_rate" : falseRejectRate,
        "half_total_error" : halfTotalError,
        "f1_score" : f1Score,
        "liveness" : liveness
    }

    print(returnObj)
    return returnObj
    

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True, port=5000)