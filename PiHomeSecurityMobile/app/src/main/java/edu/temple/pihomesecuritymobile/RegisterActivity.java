package edu.temple.pihomesecuritymobile;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import edu.temple.pihomesecuritymobile.models.Response;

public class RegisterActivity extends AppCompatActivity {
    SharedPreferences sharePref;
    ContentManager contentManager = new ContentManager();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        setTitle("Register");
        sharePref = getSharedPreferences("PREF_NAME",MODE_PRIVATE);
        Button login = findViewById(R.id.loginButton);
        login.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(RegisterActivity.this,LoginActivity.class);
                startActivity(intent);
            }
        });
        Button register = findViewById(R.id.registerButton);
        register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String[] form = createRegisterForm();
                if(form != null){
                    sharePref.edit().putBoolean("Registered",true).apply();
                    Intent intent = new Intent(RegisterActivity.this,MainActivity.class);
                    intent.putExtra("form",form);
                    startActivity(intent);
                }
            }
        });
    }

    public String[] createRegisterForm(){
        Response response = new Response();
        EditText username = findViewById(R.id.editText4);
        EditText homeAddr = findViewById(R.id.editText3);
        EditText password = findViewById(R.id.editText5);
        EditText confirm = findViewById(R.id.editText6);
        EditText homePin = findViewById(R.id.pinText);
        EditText phoneNumber = findViewById(R.id.phoneNumText);
        long phoneNum;
        if(username.getText().toString().equals("") && homeAddr.getText().toString().equals("") && password.getText().toString().equals("")
                && homePin.getText().toString().equals("") && phoneNumber.getText().toString().equals("")){
            Toast.makeText(getApplicationContext(),"Some fields have been left empty", Toast.LENGTH_SHORT).show();
            return null;
        }
        if(!confirm.getText().toString().equals(password.getText().toString())){
            Toast.makeText(getApplicationContext(),"Passwords do not match", Toast.LENGTH_SHORT).show();
            return null;
        }
        if (phoneNumber.getText().toString().length()!=10) {
            Toast.makeText(getApplicationContext(),"Please enter a valid phone number with no dashes or symbols.", Toast.LENGTH_SHORT).show();
            return null;
        }
        try {
            phoneNum = Long.parseLong(phoneNumber.getText().toString());
            Log.d("Phone number", "" + Long.toString(phoneNum));
        } catch(NumberFormatException nfe) {
            Toast.makeText(getApplicationContext(),"Please enter a valid phone number.", Toast.LENGTH_SHORT).show();
            Log.d("NumberFormatException", "" + nfe.toString());
            return null;
        }
        // see if pin matches and if home address exists in database
        String result = contentManager.selectIDStatement("HomeAccount", "AccountPin, AccountID", "HomeAccountAddress", "'" + homeAddr.getText().toString() + "'");
        Log.d("TEST_REG_LOOKUP", "" + result);
        String accountID;
        try {
            JSONObject jsonObject = new JSONObject(result);
            if (jsonObject.getInt("statusCode")==contentManager.records_not_exist) {
                Toast.makeText(getApplicationContext(),"Home address not registered", Toast.LENGTH_SHORT).show();
                return null;
            }
            response.setBody(jsonObject.getString("body"));
            //Log.d("pin", "" + response.getBody().getString("AccountPin"));
            if(!homePin.getText().toString().equals(response.getBody().getString("AccountPin"))){
                Toast.makeText(getApplicationContext(),"Incorrect pin used", Toast.LENGTH_SHORT).show();
                return null;
            }
            accountID = response.getBody().getString("AccountID");
        } catch (JSONException e) {
            e.printStackTrace();
            return null;
        }

        String deviceId = android.provider.Settings.Secure.getString(getContentResolver(), android.provider.Settings.Secure.ANDROID_ID);

        Toast.makeText(getApplicationContext(),"Registering", Toast.LENGTH_SHORT).show();
        //Log.d("Response result", "Pin and ID: " + response.getBodyString());

        result = contentManager.insertStatement("UserAccounts", "AccountID, Username, UserPassword, UserPhoneNumber, MasterUserFlag, PhoneId",
                "'" + accountID + "','" + username.getText().toString() + "','" + password.getText().toString() + "'," + phoneNum + ",'" + "1" + "','" + deviceId + "'");
        Log.d("result", "" + result);
        String[] registerForm = {username.getText().toString(),homeAddr.getText().toString(),password.getText().toString(), homePin.getText().toString()};
        return registerForm;
    }

}
