package com.example.myapplication;

import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;
import java.util.HashMap;

public class ClassifyResponse {
    @SerializedName("status")
    int status;

    @SerializedName("accuracy_score")
    double accuracyScore;

    @SerializedName("half_total_error")
    double halfTotalError;

    @SerializedName("false_accept_rate")
    double falseAcceptRate;

    @SerializedName("false_reject_rate")
    double falseRejectRate;

    @SerializedName("f1_score")
    double f1Score;

    @SerializedName("liveness")
    int liveness;

    @SerializedName("machine_learning_algorithm")
    String machineLearningAlgorithm;

    public double getAccuracyScore() {
        return accuracyScore;
    }

    public double getHalfTotalError() {
        return halfTotalError;
    }

    public double getFalseAcceptRate() {
        return falseAcceptRate;
    }

    public double getF1Score() {
        return f1Score;
    }

    public double getFalseRejectRate() {
        return falseRejectRate;
    }

    public int getLiveness() {
        return liveness;
    }

    public String getMachineLearningAlgorithm() {
        return machineLearningAlgorithm;
    }

    int getStatus() {
        return status;
    }
}
