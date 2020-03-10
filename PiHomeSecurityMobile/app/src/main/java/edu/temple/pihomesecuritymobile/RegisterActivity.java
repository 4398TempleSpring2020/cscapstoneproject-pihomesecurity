package edu.temple.pihomesecuritymobile;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class RegisterActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        setTitle("Register");
        EditText homeID = findViewById(R.id.editText3);
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

                }
            }
        });
    }

    public String[] createRegisterForm(){
        EditText homeID = findViewById(R.id.editText4);
        EditText homeAddr = findViewById(R.id.editText3);
        EditText userID = findViewById(R.id.editText5);
        if(homeID.getText().toString().equals("") && homeAddr.getText().toString().equals("") && userID.getText().toString().equals("")){
            Toast.makeText(getApplicationContext(),"Some fields have been left empty", Toast.LENGTH_SHORT).show();
            return null;
        }
        Toast.makeText(getApplicationContext(),"Registering", Toast.LENGTH_SHORT).show();
        String[] registerForm = {homeID.getText().toString(),homeAddr.getText().toString(),userID.getText().toString()};
        return registerForm;
    }

}
