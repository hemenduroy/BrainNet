package com.example.myapplication;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;

public interface Endpoints {
    @GET("get-brain-signals")
    Call<ServerResponse> getSignals();

    @POST("classify-brain-signals")
    Call<ClassifyResponse> classifySignals(@Body JSONObject body);
}
