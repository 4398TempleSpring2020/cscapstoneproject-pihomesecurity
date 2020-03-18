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

    /**
     * Primary method to do registration stuff in
     * ensures each entry text field is filled out correctly, home address exists in database already,
     * and that pin matches home address pin, and then sends registration data to the database
     * @return String array of user data
     */
    public String[] createRegisterForm(){
        Response response;
        EditText username = findViewById(R.id.editText4);
        EditText homeAddr = findViewById(R.id.editText3);
        EditText password = findViewById(R.id.editText5);
        EditText confirm = findViewById(R.id.editText6);
        EditText homePin = findViewById(R.id.pinText);
        EditText phoneNumber = findViewById(R.id.phoneNumText);
        String newUser = username.getText().toString().trim();
        String newPass = password.getText().toString().trim();
        String address = homeAddr.getText().toString().trim();
        String phone = phoneNumber.getText().toString().trim();
        String pin = homePin.getText().toString().trim();
        long phoneNum;
        //ensure each field is filled out
        if(newUser.equals("") && address.equals("") && newPass.equals("") && confirm.getText().toString().trim().equals("")
                && pin.equals("") && phone.equals("")){
            if (newUser.equals("")) {
                username.setError("Field is empty");
            }
            if (newPass.equals("")) {
                password.setError("Field is empty");
            }
            if (address.equals("")) {
                homeAddr.setError("Field is empty");
            }
            if (pin.equals("")) {
                homePin.setError("Field is empty");
            }
            if (phone.equals("")) {
                phoneNumber.setError("Field is empty");
            }
            if (confirm.getText().toString().trim().equals("")) {
                confirm.setError("Field is empty");
            }
            Toast.makeText(getApplicationContext(),"Some fields have been left empty", Toast.LENGTH_SHORT).show();
            return null;
        }
        //ensure password and confirm password match
        if(!confirm.getText().toString().equals(newPass)) {
            confirm.setError("Passwords do not match");
            password.setError("Passwords do not match");
            Toast.makeText(getApplicationContext(),"Passwords do not match", Toast.LENGTH_SHORT).show();
            return null;
        }
        //ensure phone number is correct length
        if (phone.length()!=10) {
            phoneNumber.setError("Please enter a phone number like 1231231234");
            Toast.makeText(getApplicationContext(),"Please enter a valid phone number with no dashes or symbols.", Toast.LENGTH_SHORT).show();
            return null;
        }
        try {
            //try to cast phone number to long
            phoneNum = Long.parseLong(phone);
            //Log.d("Phone number", "" + Long.toString(phoneNum));
        } catch(NumberFormatException nfe) {
            phoneNumber.setError("Please enter a phone number like 1231231234");
            Toast.makeText(getApplicationContext(),"Please enter a valid phone number.", Toast.LENGTH_SHORT).show();
            Log.d("NumberFormatException", "" + nfe.toString());
            return null;
        }
        //check if home address exists in database, will use LIKE instead of = in lambda so only street address needs to match
        String result = contentManager.selectIDStatement("HomeAccount", "AccountPin, AccountID, NumOfUsers", "HomeAccountAddress", "'" + address + "'");
        Log.d("LOOKUP_ADDRESS", "" + result);
        //put result into a response object
        response = contentManager.makeResponse(result);
        //see if we got a status code signaling home address does not exist
        if (response.getStatusCode()==contentManager.records_not_exist) {
            homeAddr.setError("Home address not found");
            Toast.makeText(getApplicationContext(),"Home address not registered", Toast.LENGTH_SHORT).show();
            return null;
        } else if (response==null) {
            Log.d("null", "response is null; error");
            return null;
        }
        String accountID;
        int numUsers;
        try {
            //check that the pin number matches what the Home Account Pin equals
            if(!pin.equals(response.getBody().getString("AccountPin"))){
                homePin.setError("Pin does not match");
                Toast.makeText(getApplicationContext(),"Incorrect pin used", Toast.LENGTH_SHORT).show();
                return null;
            }
            accountID = response.getBody().getString("AccountID");
            numUsers = Integer.parseInt(response.getBody().getString("NumOfUsers"));
        } catch (JSONException e) {
            e.printStackTrace();
            return null;
        } catch(NumberFormatException nfe) {
            nfe.printStackTrace();
            return null;
        }

        //get device id for database entry
        String deviceId = android.provider.Settings.Secure.getString(getContentResolver(), android.provider.Settings.Secure.ANDROID_ID);
        if (deviceId == null) {
            deviceId = "";
        }

        Toast.makeText(getApplicationContext(),"Registering", Toast.LENGTH_SHORT).show();
        //Log.d("Response result", "Pin and ID: " + response.getBodyString());

        //insert new user into database
        result = contentManager.insertStatement("UserAccounts", "AccountID, Username, UserPassword, UserPhoneNumber, MasterUserFlag, PhoneId",
                "'" + accountID + "','" + newUser + "','" + newPass + "'," + phoneNum + ",'" + "1" + "','" + deviceId + "'");
        //Log.d("result", "insert: " + result);
        //increment number of users for home account
        numUsers +=1;
        //Log.d("numusers", Integer.toString(numUsers));
        //update home account with new number of users
        result = contentManager.updateStatement("HomeAccount", "NumOfUsers", "'" + numUsers + "'", "AccountID", accountID);
        //Log.d("result", "update: " + result);
        String[] registerForm = {newUser, address, newPass, pin};
        return registerForm;
    }

}
