package edu.temple.pihomesecuritymobile;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;

public class MainEmptyActivity extends AppCompatActivity {
    SharedPreferences sharePref;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_empty);
        Intent intent;

        if(true){
            intent = new Intent(this,RegisterActivity.class);
            startActivity(intent);
        } else{
            intent = new Intent(this,MainActivity.class);
            startActivity(intent);
        }
    }
}
