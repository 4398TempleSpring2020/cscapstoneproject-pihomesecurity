package edu.temple.pihomesecuritymobile;

import android.util.JsonWriter;
import android.util.Log;

import java.io.*;
import java.net.*;

import org.json.JSONException;
import org.json.JSONObject;

class ListenerThread extends Thread {
    String ipAddr;
    int port;
    Socket clientSocket;

    public ListenerThread(String ip, int port, Socket socket) {
        this.ipAddr = ip;
        this.port = port;
        this.clientSocket = socket;

    }


    public void run() {
        Log.d("client_test","Thread " + Thread.currentThread().getId() + " handling listener side connection from : "
                + ipAddr + ":" + port);

        while (true) {
            try {
                //input
                DataInputStream dis = new DataInputStream(clientSocket.getInputStream());

                while (true) {
                    String data = "";
                    try {
                        data = dis.readUTF();
                        Log.d("client_test","data received : " + data);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    if (data.equals("exit")) {
                        Log.d("client_test","Closing this connection : " + clientSocket);
                        clientSocket.close();
                        Log.d("client_test","Connection closed");
                        break;
                    }
                }
                // closing resources
                dis.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}

// Client class
public class Client {

    String host;
    int port;
    Socket client_socket;
    OutputStream output;
    Writer writer;
    BufferedWriter buffer;

    public Client(String host, int port) {
        this.host = host;
        this.port = port;
        writer = new Writer() {
            @Override
            public void write(char[] chars, int i, int i1) throws IOException {

            }

            @Override
            public void flush() throws IOException {

            }

            @Override
            public void close() throws IOException {

            }
        };
        buffer = new BufferedWriter(writer);
    }



    public boolean send(JSONObject json){
        try {
            this.buffer.write(json.toString());
            this.buffer.flush();
            return true;
        }
        catch(Exception e){
            e.printStackTrace();
            Log.d("client_test","Error sending data");
            return false;}
    }
    public void start(){
        try {
            InetAddress ip = InetAddress.getByName("localhost");
            System.out.println(ip);
            // establish the connection with server port 5056
            this.client_socket = new Socket("192.168.0.11", 5000);
            Log.d("client_test","connected to server");
            this.output = this.client_socket.getOutputStream();
            this.writer = new OutputStreamWriter(this.output);
            this.buffer = new BufferedWriter(this.writer);
            this.buffer.flush();

            Thread listener_thread = new ListenerThread(host, port, client_socket);
            listener_thread.start();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
