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

import java.util.UUID;

// uses https://developer.android.com/guide/topics/connectivity/bluetooth#java for bluetooth connection and set up

public class MainActivity extends AppCompatActivity implements OnRequestPermissionsResultCallback {

    final private int REQUEST_ENABLE_BT = 3;
    final private int REQUEST_READ_PHONE_STATE = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        int permissionCheck = ContextCompat.checkSelfPermission(this, Manifest.permission.READ_PHONE_STATE);

        if (permissionCheck != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.READ_PHONE_STATE}, REQUEST_READ_PHONE_STATE);
        } else {
            //TODO
        }
        BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        Log.d("DEBUG", "Did start");
        if(bluetoothAdapter == null){
            Log.d("DEBUG", "adapter null");
            AlertDialog.Builder alert = new AlertDialog.Builder(getApplicationContext());
            alert.setTitle("Bluetooth Error");
            alert
                    .setMessage("This Phone does not support Bluetooth")
                    .setCancelable(false)
                    .setPositiveButton("Exit", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            dialogInterface.cancel();
                        }
                    });
            Toast.makeText(getApplicationContext(),"Bluetooth Error",Toast.LENGTH_LONG).show();
        } else {
            Toast.makeText(getApplicationContext(),"Bluetooth Allowed",Toast.LENGTH_LONG).show();
        }
        if(!bluetoothAdapter.isEnabled()){
            Log.d("DEBUG", "bluetooth not enabled");
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
        }
        TelephonyManager tMananger = (TelephonyManager)getSystemService(getApplicationContext().TELEPHONY_SERVICE);
        String uuid = tMananger.getDeviceId();
        BeaconThread a = new BeaconThread(bluetoothAdapter,uuid);
        a.start();

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case REQUEST_READ_PHONE_STATE:
                if ((grantResults.length > 0) && (grantResults[0] == PackageManager.PERMISSION_GRANTED)) {

                }
                break;

            default:
                break;
        }
    }
}
