package com.example.myapplication;

import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.File;

public class PermissionsHandler extends AppCompatActivity {
    Context context;
    public static int STORAGE_PERMISSION_CODE;
    Activity activity;

    PermissionsHandler(Context context, final int code, Activity activity){
        this.context = context;
        this.STORAGE_PERMISSION_CODE = code;
        this.activity = activity;
    }

    public void checkPermission(String permission)
    {
        if (ContextCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED) {

            // Requesting the permission
            try {
                ActivityCompat.requestPermissions(activity, new String[]{permission}, STORAGE_PERMISSION_CODE);
            } catch (Exception e) {
                System.out.println("Exception while requesting permissions " + e);
            }
        }
        else {
            System.out.println("Permission already granted");
//            Toast.makeText(activity, "Permission already granted", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           @NonNull String[] permissions,
                                           @NonNull int[] grantResults)
    {
        super.onRequestPermissionsResult(requestCode,
                permissions,
                grantResults);

        if (requestCode == STORAGE_PERMISSION_CODE) {
            if (grantResults.length > 0
                    && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                System.out.println("Permission already granted");

            } else {
                Toast.makeText(activity, "Storage Permission Denied", Toast.LENGTH_SHORT).show();
            }
        }
    }
}