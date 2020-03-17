package edu.temple.pihomesecuritymobile;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class RegisterActivity extends AppCompatActivity {
    SharedPreferences sharePref;
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
        EditText homeID = findViewById(R.id.editText4);
        EditText homeAddr = findViewById(R.id.editText3);
        EditText password = findViewById(R.id.editText5);
        EditText confirm = findViewById(R.id.editText6);
        if(homeID.getText().toString().equals("") && homeAddr.getText().toString().equals("") && password.getText().toString().equals("")){
            Toast.makeText(getApplicationContext(),"Some fields have been left empty", Toast.LENGTH_SHORT).show();
            return null;
        }
        if(!confirm.getText().toString().equals(password.getText().toString())){
            Toast.makeText(getApplicationContext(),"Passwords do not match", Toast.LENGTH_SHORT).show();
            return null;
        }
        Toast.makeText(getApplicationContext(),"Registering", Toast.LENGTH_SHORT).show();
        String[] registerForm = {homeID.getText().toString(),homeAddr.getText().toString(),password.getText().toString()};
        return registerForm;
    }

}
