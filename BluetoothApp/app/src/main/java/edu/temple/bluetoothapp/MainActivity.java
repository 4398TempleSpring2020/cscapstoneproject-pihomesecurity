package edu.temple.bluetoothapp;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.app.ActivityCompat.OnRequestPermissionsResultCallback;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.widget.Toast;

import org.altbeacon.beacon.Beacon;

import java.util.UUID;

// uses https://developer.android.com/guide/topics/connectivity/bluetooth#java for bluetooth connection and set up

public class MainActivity extends AppCompatActivity implements OnRequestPermissionsResultCallback {

    final private int REQUEST_ENABLE_BT = 3;
    final private int REQUEST_READ_PHONE_STATE = 1;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
    }
}
