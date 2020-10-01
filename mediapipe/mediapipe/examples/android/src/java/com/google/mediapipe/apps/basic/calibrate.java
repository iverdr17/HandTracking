package com.google.mediapipe.apps.basic;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class calibrate extends AppCompatActivity {
    public static int[] calib;
    int planeone, planetwo, interval, count;
    EditText intervalinput, planeoneinput, planetwoinput, countinput;
    Button startCalibration;
    private static final String TAG = "calibrateop";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.calibrate);
        planeoneinput = (EditText) findViewById(R.id.planeone);
        planetwoinput = (EditText) findViewById(R.id.planetwo);
        intervalinput = (EditText) findViewById(R.id.interval);
        countinput = (EditText) findViewById(R.id.count);
        startCalibration = (Button) findViewById(R.id.startCalibration);
        planeone = 300;
        planetwo = 600;
        interval = 100;
        count = 1;
        Log.d(TAG, planeoneinput + " " + planetwoinput + " " + intervalinput + " " + countinput);
        startCalibration.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                planeone = Integer.valueOf(planeoneinput.getText().toString());
                planetwo = Integer.valueOf(planetwoinput.getText().toString());
                interval = Integer.valueOf(intervalinput.getText().toString());
                count = Integer.valueOf(countinput.getText().toString());
                startActivity(new Intent(calibrate.this, calibrate.class));
            }
        });


    }

    public int[] calibration() {
        int[] calib = {planeone, planetwo, interval, count};
        return calib;
/*    private void showToast(String text)
    {
        Toast.makeText(calibrate.this,text,Toast.LENGTH_SHORT).show();
    }
*/
    }
}