package edu.temple.bluetoothapp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.os.Build;
import android.util.Log;

import java.util.UUID;

// uses https://developer.android.com/guide/topics/connectivity/bluetooth#java for bluetooth connection and set up

public class BeaconThread extends Thread {

    private final BluetoothServerSocket mmSock;

    public BeaconThread(BluetoothAdapter adapter,String uuid){
        BluetoothServerSocket tmp = null;
        try{
            tmp = adapter.listenUsingRfcommWithServiceRecord(Build.MODEL,UUID.fromString(uuid));
            Log.d("BLUETOOTH SOCKET UPDATE", "BeaconThread: ");
        } catch (Exception e){
            Log.e("BT error", "Problem connecting to bluetooth", e);
        }
        mmSock = tmp;

    }

    public void run(){
        BluetoothSocket sock = null;
        Log.d("SOCKET starts", "start called");
        while(true){
            try{
                sock = mmSock.accept();
            } catch (Exception e){
                Log.e("BT ACCEPT FAILS", "Problem connecting to bluetooth", e);
                break;
            }
            if(sock == null){
                try{
                    mmSock.close();
                    Log.d("SOCKET CLOSED", "SOCKET CLOSED");
                } catch (Exception e){
                    Log.e("SOCKET CLOSE FAILS", "Problem closing socket",e );
                }
                break;
            }
        }

    }
}
