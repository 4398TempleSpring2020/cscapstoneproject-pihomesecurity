package edu.temple.pihomesecuritymobile;


import android.content.Context;
import android.os.AsyncTask;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

import edu.temple.pihomesecuritymobile.models.Request;
import edu.temple.pihomesecuritymobile.models.Response;

/**
 * ContentManager is the class that deals with connecting to the API and sending POST/GET requests
 */
public class ContentManager {
    //the base url
    final private String base_url = "https://jlt49k4n90.execute-api.us-east-2.amazonaws.com/beta";
    private static Response response = new Response();
    private AsyncListener activity;

    //resource paths
    final private String show_record_resource="/show";
    final private String insert_resource="/insert";
    final private String update_resource="/update";
    final private String delete_resource="/delete";

    //resource required keys in JSONObject
    final private String[] show_all_keys = new String[] {"table", "columns"};
    final private String[] show_record_keys = new String[] {"table", "columns", "columnMatch", "valueMatch"};
    final private String[] insert_keys = new String[] {"table", "columns", "values"};
    final private String[] update_keys = new String[] {"table", "column", "newColVal", "row", "rowVal"};
    final private String[] delete_keys = new String[] {"table", "column", "value"};

    public ContentManager(Context context) {
        this.activity = (AsyncListener)context;
    }
    /**
     * This method is the one that gets called from the Activity that needs to make a POST/GET request
     * @param method: "GET" or "POST"
     * @param resource: To know which resource path to call cause they all have their own lambda functions
     * @param body: the JSONObject that is gonna get passed through the POST method
     */
    private void requestData(String method, String resource, JSONObject body) {
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
     * @return String that is a response from the server
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

                //Log.d("RESPONSE CODE", "response code: " + con.getResponseCode());
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
    private class Downloader extends AsyncTask<Request, Void, String> {

        /**
         * This gets ran in background asynchronously to start network stuff.
         * @param params: requires an array sent as parameter I think but we really only ever send
         *              one Request to it
         * @return String that gets sent to the onPostExecute() method below as a parameters
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
                response.setStatusCode(jsonObject.getInt("statusCode"));
                response.setMessage(jsonObject.getString("message"));
                response.setBody(jsonObject.getString("body"));
                //Log.d("STATUSCODE", "status code: " + response.getStatusCode());
                //Log.d("MESSAGE", "message: " + response.getMessage());
                //Log.d("RESPONSE", "body: " + response.getBodyString());
                activity.doAfterAsync(response);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * Interface required to get the data returned
     */
    public interface AsyncListener{
        void doAfterAsync(Response nresponse);
    }

    /**
     * Example of GET request
     * Returns a list of tables in the database, isn't really meant for us
     * SQL used in lambda: SHOW TABLES;
     */
    void showTables() {
        requestData("GET", "", new JSONObject());
    }

    /**
     * Example of POST request to return all records in a table with the specified columns
     * SQL used in lambda: SELECT columns FROM table;
     * @param table: table to get records from
     * @param columns: columns to show
     */
    void selectStatement(String table, String columns) {
        JSONObject params = new JSONObject();
        try {
            params.put(show_all_keys[0], table);
            params.put(show_all_keys[1], columns);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        requestData("POST", "", params);
    }

    /**
     * Example of a POST statement that returns a record matching a specified value
     * SQL used in lambda: SELECT columns FROM table WHERE columnMatch = valueMatch
     * @param table: table to get record from
     * @param columns: columns to show
     * @param columnMatch: column that value will match
     * @param valueMatch: value to match
     */
    void selectIDStatement(String table, String columns, String columnMatch, String valueMatch) {
        JSONObject params = new JSONObject();
        try {
            params.put(show_record_keys[0], table);
            params.put(show_record_keys[1], columns);
            params.put(show_record_keys[2], columnMatch);
            params.put(show_record_keys[3], valueMatch);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        requestData("POST", show_record_resource, params);
    }

    /**
     * Example of a POST statement that inserts a new record
     * SQL used in lambda: INSERT INTO table (columns) VALUES (values);
     * @param table: table to add new record to
     * @param columns: columns to insert values in
     * @param values: values to be inserted
     */
    protected void insertStatement(String table, String columns, String values) {
        JSONObject params = new JSONObject();
        try {
            params.put(insert_keys[0], table);
            params.put(insert_keys[1], columns);
            params.put(insert_keys[2], values);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        requestData("POST", insert_resource, params);
    }

    /**
     * Example of a POST statement that deletes a record matching a specified value
     * SQL used in lambda: DELETE FROM table WHERE column = value;
     * @param table: table to delete record from
     * @param columnMatch: column to match value with
     * @param valueMatch: value to match
     */
    protected void deleteStatement(String table, String columnMatch, String valueMatch) {
        JSONObject params = new JSONObject();
        try {
            params.put(delete_keys[0], table);
            params.put(delete_keys[1], columnMatch);
            params.put(delete_keys[2], valueMatch);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        requestData("POST", delete_resource, params);
    }

    /**
     * Example of a POST statement that updates a record matching a specified value
     * SQL used in lambda: UPDATE table SET column = newColValue WHERE row = rowVal;
     * @param table: table to update
     * @param newColumn: column to place new value in
     * @param newValue: value to replace old value with
     * @param columnMatch: column to match value with
     * @param valueMatch: value to match
     */
    protected void updateStatement(String table, String newColumn, String newValue, String columnMatch, String valueMatch) {
        JSONObject params = new JSONObject();
        try {
            params.put(update_keys[0], "Employee");
            params.put(update_keys[1], "EmployeeName");
            params.put(update_keys[2], "'New Employee'");
            params.put(update_keys[3], "EmployeeID");
            params.put(update_keys[4], "1");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        requestData("POST", update_resource, params);
    }
}

