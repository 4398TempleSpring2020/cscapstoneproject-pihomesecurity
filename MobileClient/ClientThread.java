package edu.temple.pihomesecuritymobile.client;

import android.util.Log;

public class ClientThread extends Thread{
private Client client;

    public ClientThread(Client c) {
        this.client = c;
    }

    public void run(){
        Log.d("client_test","Starting Server Thread...");
        client.start();
    }
}
