package edu.temple.bluetoothapp;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    final private int REQUEST_ENABLE_BT = 3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
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


    }
}
