package com.example.myapplication;

import com.google.gson.JsonObject;
import com.google.gson.annotations.SerializedName;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

public class ServerResponse {
    @SerializedName("status")
    int status;

    @SerializedName("brain_signals")
    ArrayList<HashMap<Integer, Double>> brainSignals;

    ArrayList<HashMap<Integer, Double>> getBrainSignals() {
        return brainSignals;
    }

    int getStatus() {
        return status;
    }
}
