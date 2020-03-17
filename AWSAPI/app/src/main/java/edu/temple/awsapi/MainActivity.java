package edu.temple.awsapi;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity implements ContentManager.AsyncListener {
    private TextView textView;
    protected static Response response = new Response();
   // protected Map<String,String> params = new HashMap<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //textView = findViewById(R.id.textview1);
        //get only returns the name of each table
        ContentManager contentManager = new ContentManager(this);
        //contentManager.showTables();
        //contentManager.selectStatement("Employee", "*");
        //contentManager.selectIDStatement("Employee", "*", "EmployeeID", "1");
        //contentManager.insertStatement("Employee", "EmployeeName, EmployeeUsername, EmployeePassword", "'Temple Employee 3', 'TUID 3', '1234'");
        //contentManager.deleteStatement("Employee", "EmployeeID", "15");
        contentManager.updateStatement("Employee", "Employee Name", "'New Employee'", "EmployeeID", "1");
    }

    /**
     * put stuff in here that you want to happen after Async network stuff done.
     * Get data from POST this way.
     * @param nresponse: Response object holding response data
     */
    public void doAfterAsync(Response nresponse) {
        response=nresponse;
        Log.d("STATUSCODE", "status code: " + response.getStatusCode());
        Log.d("MESSAGE", "message: " + response.getMessage());
        Log.d("RESPONSE", "body: " + response.getBodyString());
    }
}


