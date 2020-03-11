package edu.temple.awsapi;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {
    private TextView textView;
   // protected Map<String,String> params = new HashMap<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //textView = findViewById(R.id.textview1);
        //get only returns the name of each table
        showTables();
        //selectStatement();
        selectIDStatement();
        //insertStatement();
        //deleteStatement();
        //updateStatement();
    }

    /**
     * Example of GET request
     * Returns a list of tables in the database, isn't really meant for us
     * SQL used in lambda: SHOW TABLES;
     */
    protected void showTables() {
        ContentManager contentManager = new ContentManager();
        contentManager.requestData("GET", "", new JSONObject());
    }

    /**
     * Example of POST request to return all records in a table with the specified columns
     * MUST have a table and columns key in the JSONObject
     * SQL used in lambda: SELECT columns FROM table;
     */
    protected void selectStatement() {
        ContentManager contentManager = new ContentManager();
        JSONObject params = new JSONObject();
        try {
            params.put("table", "Employee");
            params.put("columns", "*");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        contentManager.requestData("POST", "", params);
    }

    /**
     * Example of a POST statement that returns a record matching a specified value
     * MUST HAVE the keys table, columns, columnMatch, and valueMatch in the JSONObject
     * POST method located at base_url + "/show"
     * Make sure to put single quotes around the matching values when they are Strings
     * SQL used in lambda: SELECT columns FROM table WHERE columnMatch = valueMatch;
     */
    protected void selectIDStatement() {
        ContentManager contentManager = new ContentManager();
        JSONObject params = new JSONObject();
        try {
            params.put("table", "Employee");
            params.put("columns", "*");
            params.put("columnMatch", "EmployeeID");
            params.put("valueMatch", "1");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        contentManager.requestData("POST", contentManager.show_record_resource, params);
    }

    /**
     * Example of a POST statement that inserts a new record
     * MUST HAVE the keys table, columns, and values in the JSONObject
     * POST method located at base_url + "/insert"
     * Make sure to put single quotes around the new inserted values when they are Strings
     * SQL used in lambda: INSERT INTO table (columns) VALUES (values);
     */
    protected void insertStatement() {
        ContentManager contentManager = new ContentManager();
        JSONObject params = new JSONObject();
        try {
            params.put("table", "Employee");
            params.put("columns", "EmployeeName, EmployeeUsername, EmployeePassword");
            params.put("values", "'Temple Employee 3', 'TUID 3', '1234'");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        contentManager.requestData("POST", contentManager.insert_resource, params);
    }

    /**
    * Example of a POST statement that deletes a record matching a specified value
    * MUST HAVE the keys table, column, and value in the JSONObject
    * POST method located at base_url + "/delete"
     * Make sure to put single quotes around the matching values when they are Strings
    * SQL used in lambda: DELETE FROM table WHERE column = value;
    */
    protected void deleteStatement() {
        ContentManager contentManager = new ContentManager();
        JSONObject params = new JSONObject();
        try {
            params.put("table", "Employee");
            params.put("column", "EmployeeID");
            params.put("value", "15");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        contentManager.requestData("POST", contentManager.delete_resource, params);
    }

    /**
     * Example of a POST statement that updates a record matching a specified value
     * MUST HAVE the keys table, column, newColVal, row, and roVal in the JSONObject
     * POST method located at base_url + "/update"
     * Make sure to put single quotes around the matching values when they are Strings
     * SQL used in lambda: UPDATE table SET column = newColValue WHERE row = rowVal;
     */
    protected void updateStatement() {
        ContentManager contentManager = new ContentManager();
        JSONObject params = new JSONObject();
        try {
            params.put("table", "Employee");
            params.put("column", "EmployeeName");
            params.put("newColVal", "'New Employee'");
            params.put("row", "EmployeeID");
            params.put("rowVal", "1");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        contentManager.requestData("POST", contentManager.update_resource, params);
    }
}


