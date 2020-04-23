package edu.temple.pihomesecuritymobile;

import android.os.SystemClock;
import android.util.JsonWriter;
import android.util.Log;

import java.io.*;
import java.net.*;

import org.json.JSONException;
import org.json.JSONObject;
/*
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
*/
// Client class
public class Client {

    String host;
    int port;
    Socket client_socket;
    OutputStream output;
    Writer writer;
    BufferedWriter buffer;
    String stuff;

    public Client(String host, int port, String message) {
        this.host = host;
        this.port = port;
        this.stuff  = message;
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
/*
    public boolean send(String stuff){
        try {
            this.buffer.write(stuff);
            this.buffer.flush();
            return true;
        }
        catch(Exception e){
            e.printStackTrace();
            Log.d("client_test","Error sending data");
            return false;}
    }
  */
    public void start(){
        try {
            //InetAddress ip = InetAddress.getByName("localhost");
            //System.out.println(ip);
            this.client_socket = new Socket(host, port);
            Log.d("client_test","connected to server");
            this.output = this.client_socket.getOutputStream();
            this.writer = new OutputStreamWriter(this.output);
            this.buffer = new BufferedWriter(this.writer);
            this.buffer.flush();
            this.buffer.write("Pi_Mobile");
            Log.d("sending Pi_Mobile", "Pi_Mobile sent");
            this.buffer.flush();
            SystemClock.sleep(10);
            this.buffer.write(stuff);
            Log.d("sending data", "" + stuff);
            this.buffer.flush();


            //Thread listener_thread = new ListenerThread(host, port, client_socket);
            //listener_thread.start();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
