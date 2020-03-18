package edu.temple.pihomesecuritymobile;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;

import edu.temple.pihomesecuritymobile.models.Response;

public class LoginActivity extends AppCompatActivity {
    SharedPreferences sharePref;
    ContentManager contentManager = new ContentManager();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        setTitle("Login");
        sharePref = getSharedPreferences("PREF_NAME",MODE_PRIVATE);
        Button login = findViewById(R.id.button);
        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String[] form = createLoginForm();
                if(form != null){
                    sharePref.edit().putBoolean("Registered",true).apply();
                    Intent intent = new Intent(LoginActivity.this,MainActivity.class);
                    intent.putExtra("form",form);
                    startActivity(intent);
                }
            }
        });
    }

    private String[] createLoginForm(){
        EditText username = findViewById(R.id.editText);
        EditText password = findViewById(R.id.editText2);
        String user = username.getText().toString().trim();
        String pass = password.getText().toString().trim();
        if(pass.equals("") || user.equals("")){
            if (user.equals("")) {
                username.setError("Field is empty");
            }
            if (pass.equals("")) {
                password.setError("Field is empty");
            }
            Toast.makeText(getApplicationContext(),"Fields have been left empty", Toast.LENGTH_SHORT).show();
            return null;
        }
        Response response;
        String result = contentManager.selectIDStatement("UserAccounts", "UserID, AccountID, Username, UserPassword, MasterUserFlag", "Username", "'" + user + "'");
        Log.d("LOOKUP_USER", "" + result);
        //put result into a response object
        response = contentManager.makeResponse(result);
        if (response.getStatusCode()==contentManager.records_not_exist) {
            username.setError("Incorrect password or username");
            password.setError("Incorrect password or username");
            Toast.makeText(getApplicationContext(),"Incorrect password or username", Toast.LENGTH_SHORT).show();
            return null;
        } else if (response==null) {
            Log.d("null", "lookup response is null; error");
            return null;
        }
        String userID;
        String accountID;
        try {
            if(!pass.equals(response.getBody().getString("UserPassword"))){
                password.setError("Incorrect password or username");
                username.setError("Incorrect password or username");
                Toast.makeText(getApplicationContext(),"Incorrect password or username", Toast.LENGTH_SHORT).show();
                return null;
            }
            userID = response.getBody().getString("UserID");
            accountID = response.getBody().getString("AccountID");
        } catch (JSONException e) {
            e.printStackTrace();
            return null;
        }

        String[] loginForm = {user, pass, accountID};
        Toast.makeText(getApplicationContext(),"Logging in...", Toast.LENGTH_SHORT).show();
        //update last login for user
        result = contentManager.updateStatement("UserAccounts", "LastLogin", "current_timestamp()", "UserID", userID);
        Log.d("UPDATE_DATE", "" + result);

        return loginForm;
    }
}
