package edu.temple.pihomesecuritymobile;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

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
            Toast.makeText(getApplicationContext(),"Fields have been left empty", Toast.LENGTH_SHORT).show();
            return null;
        }
        String[] loginForm = {user, pass};
        Toast.makeText(getApplicationContext(),"Logging in...", Toast.LENGTH_SHORT).show();
        return loginForm;
    }
}
