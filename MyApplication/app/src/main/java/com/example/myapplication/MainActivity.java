package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {
    Button receiveBrainSignals;
    Button classifyBrainSignals;
    TextView predictionOutput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        PermissionsHandler permissionsHandler = new PermissionsHandler(MainActivity.this, 2, MainActivity.this);
        permissionsHandler.checkPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        receiveBrainSignals = findViewById(R.id.receive_brain_signals);
        classifyBrainSignals = findViewById(R.id.classify_brain_signals);
        predictionOutput = findViewById(R.id.classified_data);
        receiveBrainSignals.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Endpoints getResponse = RetrofitClient.getRetrofitInstance().create(Endpoints.class);
                Call<ServerResponse> apiCall = getResponse.getSignals();
                apiCall.enqueue(new Callback<ServerResponse>() {
                    @Override
                    public void onResponse(Call<ServerResponse> call, Response<ServerResponse> response) {
                        Gson gson = new Gson();
                        ServerResponse serverResponse = response.body();
                        ArrayList<HashMap<Integer, Double>> brainSignalData= serverResponse.getBrainSignals();
                        HashMap<String, ArrayList<HashMap<Integer, Double>>> jsonBody = new HashMap<>();
                        jsonBody.put("brain_signals", brainSignalData);
                        JsonObject json = gson.toJsonTree(jsonBody).getAsJsonObject();
                        System.out.println(json);

                        try {
                            File jsonFileName = new File(Environment.getExternalStorageDirectory(),"brain_signals.json");
                            if(jsonFileName.exists())
                                jsonFileName.delete();
                            jsonFileName.createNewFile();
                            System.out.println(Environment.getExternalStorageDirectory());
                            FileWriter writer = new FileWriter(jsonFileName);
                            writer.write(json.toString());
                            writer.close();
                            Toast.makeText(MainActivity.this, "Received Brain Signal(s)",
                                    Toast.LENGTH_LONG).show();
                        } catch(Exception e) {
                            e.printStackTrace();
                            System.out.println("Error occurred");
                        }
                    }

                    @Override
                    public void onFailure(Call<ServerResponse> call, Throwable t) {
                        System.out.println("Failed");
                        System.out.println(t.getMessage());
                    }
                });
            }
        });

        classifyBrainSignals.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    File jsonFileName = new File(Environment.getExternalStorageDirectory(),"brain_signals.json");
                    FileReader fileReader = new FileReader(jsonFileName);
                    BufferedReader bufferedReader = new BufferedReader(fileReader);
                    StringBuilder stringBuilder = new StringBuilder();
                    String line = bufferedReader.readLine();
                    while (line != null){
                        stringBuilder.append(line).append("\n");
                        line = bufferedReader.readLine();
                    }
                    bufferedReader.close();
                    String json = stringBuilder.toString();
                    JSONObject body = new JSONObject(json);
                    Endpoints getResponse = RetrofitClient.getRetrofitInstance().create(Endpoints.class);
                    Call<ClassifyResponse> apiCall = getResponse.classifySignals(body);
                    apiCall.enqueue(new Callback<ClassifyResponse>() {
                        @Override
                        public void onResponse(Call<ClassifyResponse> call, Response<ClassifyResponse> response) {
                            ClassifyResponse classifyResponse = response.body();
                            double accuracyScore = classifyResponse.getAccuracyScore()*100;
                            double f1Score = classifyResponse.getF1Score();
                            double falseAcceptRate = classifyResponse.getFalseAcceptRate();
                            double falseRejectRate = classifyResponse.getFalseRejectRate();
                            double halfTotalError = classifyResponse.getHalfTotalError();
                            String machineLearningAlgorithm = classifyResponse.getMachineLearningAlgorithm();
                            int liveness = classifyResponse.getLiveness();
                            if(accuracyScore > -1) {
                                DecimalFormat df = new DecimalFormat("#.000");
                                String formattedAccuracy = df.format(accuracyScore) + "%";
                                String formattedF1Score = df.format(f1Score);
                                String formattedFalseRejectRate = df.format(falseRejectRate);
                                String formattedFalseAcceptRate = df.format(falseAcceptRate);
                                String formattedHalfTotalError = df.format(halfTotalError);
                                String output = "Machine Learning Algorithm : "+ machineLearningAlgorithm + "\n"+
                                        "Accuracy : "+formattedAccuracy +"\n" +
                                        "F1 Score : "+ formattedF1Score + "\n" +
                                        "False Reject Rate : "+ formattedFalseRejectRate + "\n" +
                                        "False Accept Rate : " + formattedFalseAcceptRate + "\n" +
                                        "Half Total Error : " + formattedHalfTotalError + "\n";
                                System.out.println(accuracyScore);
                                predictionOutput.setText(output);
                            } else {
                                String output = "The signal is  ";
                                if(liveness == 0) {
                                    output += "live";
                                } else {
                                    output = "fake";
                                }
                                predictionOutput.setText(output);
                            }

                        }

                        @Override
                        public void onFailure(Call<ClassifyResponse> call, Throwable t) {
                            System.out.println("Here");
                            System.out.println(t.getMessage());
                        }
                    });
                } catch(Exception e) {
                    e.printStackTrace();
                    System.out.println("Error occurred");
                }
            }
        });
    }
}