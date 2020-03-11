package edu.temple.awsapi;


import android.os.AsyncTask;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * ContentManager is the class that deals with connecting to the API and sending POST/GET requests
 */
public class ContentManager {
    //stuff we care about in the response
    protected int statusCode=0;
    protected String message="";
    protected String response="";

    //the base url
    final protected String base_url = "https://jlt49k4n90.execute-api.us-east-2.amazonaws.com/beta";

    //resource paths
    final protected String show_record_resource="/show";
    final protected String insert_resource="/insert";
    final protected String update_resource="/update";
    final protected String delete_resource="/delete";

    //resource required keys in JSONObject
    final protected String[] show_all_keys = new String[] {"table", "columns"};
    final protected String[] show_record_keys = new String[] {"table", "columns", "columnMatch", "valueMatch"};
    final protected String[] insert_keys = new String[] {"table", "columns", "values"};
    final protected String[] update_keys = new String[] {"table", "column", "newColVal", "row", "rowVal"};
    final protected String[] delete_keys = new String[] {"table", "column", "value"};

    /**
     * This method is the one that gets called from the Activity that needs to make a POST/GET request
     * @param method: "GET" or "POST"
     * @param resource: To know which resource path to call cause they all have their own lambda functions
     * @param body: the JSONObject that is gonna get passed through the POST method
     */
    void requestData(String method, String resource, JSONObject body) {
        //our Request object contains all the stuff we need to do a successful POST method
        Request request = new Request();
        request.setMethod(method);
        request.setUrl(base_url + resource);
        request.setBody(body);
        Downloader downloader = new Downloader(); //Instantiation of the Async task
        downloader.execute(request);
    }

    /**
     * This method does all the actual connection and network and POST stuff in it.
     * @param request: contains the Request object that has the stuff we need
     * @return: String that is a response from the server
     */
    private static String getData(Request request) {
        BufferedReader reader = null;
        String uri = request.getUrl();
        try {
            URL url = new URL(uri);
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod(request.getMethod());
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("Accept", "application/json");

            if (request.getMethod().equals("POST")) {
                con.setDoInput(true);
                con.setDoOutput(true);

                //go and POST the JSONObject to the API now
                OutputStreamWriter outputStreamWriter = new OutputStreamWriter(con.getOutputStream());
                outputStreamWriter.write(request.getBody().toString());
                outputStreamWriter.flush();
                outputStreamWriter.close();

                Log.d("RESPONSE CODE", "response code: " + con.getResponseCode());
            }

            //get the response from the API
            StringBuilder sb = new StringBuilder();
            reader = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line + "\n");
            }

            return sb.toString();

        } catch (Exception e) {
            e.printStackTrace();
            return null;
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                    return null;
                }
            }
        }
    }

    /**
     * New class gets made in another class cause I don't feel it needs its' own file.
     * The connection to the API needs to be down in an AsyncTask because android does not like it
     * when you do network connection stuff on the same thread as UI stuff
     */
    private class Downloader extends AsyncTask<Request, String, String> {

        /**
         * This gets ran in background asynchronously to start network stuff.
         * @param params: requires an array sent as parameter I think but we really only ever send
         *              one Request to it
         * @return: String that gets sent to the onPostExecute() method below as a parameters
         */
        @Override
        protected String doInBackground(Request... params) {
            return ContentManager.getData(params[0]);
        }

        /**
         * This method gets executed right after doInBackground() completes its stuff.
         * @param result: the string returned from doInBackground()
         */
        @Override
        protected void onPostExecute(String result) {
            try {
                super.onPostExecute(result);
                //convert the string to a JSONObject
                JSONObject jsonObject = new JSONObject(result);

                //maybe we want to see statusCode and message in a later functionality
                statusCode =jsonObject.getInt("statusCode");
                message = jsonObject.getString("message");
                response = jsonObject.getString("body");
                Log.d("STATUSCODE", "status code: " + statusCode);
                Log.d("MESSAGE", "message: " + message);
                Log.d("RESPONSE", "body: " + response);

            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }
}

