package edu.temple.pihomesecuritymobile;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import org.json.JSONException;
import org.json.JSONObject;

import edu.temple.pihomesecuritymobile.ui.dashboard.DashboardFragment;
import edu.temple.pihomesecuritymobile.ui.home.HomeFragment;
import edu.temple.pihomesecuritymobile.ui.notifications.NotificationsFragment;

public class MainActivity extends AppCompatActivity implements HomeFragment.soundButtonListener, DashboardFragment.onFragListener, NotificationsFragment.onFragListener {
    SharedPreferences sharePrefs;
    Client client;
    ClientThread clientThread;
    final String HOST ="3.16.163.252";
    final int PORT = 5002;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        BottomNavigationView navView = findViewById(R.id.nav_view);
        Bundle formBundle = getIntent().getExtras();
        //client = new Client("3.16.163.252",5002);
        //clientThread = new ClientThread(client);
        //clientThread.start();
        sharePrefs = getSharedPreferences("PREF_NAME",MODE_PRIVATE);
        if(formBundle != null){
            String form[] = formBundle.getStringArray("form");
            sharePrefs.edit().putString("HomeID",form[0]).apply();
            sharePrefs.edit().putString("UserName",form[1]).apply();
        }
        String username = sharePrefs.getString("UserName", "");
        if (username!=null) {
            Log.d("username", "" + username);
            ContentManager contentManager = new ContentManager();
            contentManager.updateStatement("UserAccounts", "LastLogin", "current_timestamp()", "Username", username);
        }
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(
                R.id.navigation_home, R.id.navigation_dashboard, R.id.navigation_notifications)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(navView, navController);

    }


    /**
    * Method: soundAlarm()
    * Purpose: to make the alarm start playing a noise to scare off an intruder
    * Parameters: None
    * Pre-Condtions: the sound button in HomeFragment has been hit
    * Post-Condition: A message is sent to the Pi
    */
    @Override
    public void soundAlarm() {
        client = new Client(HOST,PORT, "PANIC");
        clientThread = new ClientThread(client);
        clientThread.start();
        Toast.makeText(getApplicationContext(),"Sounding Alarm", Toast.LENGTH_SHORT).show();

    }

    /**
     * Method: setAlarm()
     * Purpose: to make the security system activate and deactivate
     * Parameters: setFlag true if alarm should be turned on or false if it should be turned off
     * Pre-Condtions: the alarm switch has been used
     * Post-Condition: A message is sent to the Pi based on the setFlag
     */
    @Override
    public void setAlarm(boolean setFlag) {
        if(setFlag){
            client = new Client(HOST,PORT, "ARM");
            clientThread = new ClientThread(client);
            clientThread.start();
        } else {
            client = new Client(HOST,PORT, "DISARM");
            clientThread = new ClientThread(client);
            clientThread.start();
        }
    }


    @Override
    public void escalateRsp() {
        client = new Client(HOST,PORT, "ESCALATE");
        clientThread = new ClientThread(client);
        clientThread.start();
    }

    @Override
    public void resolveRsp() {
        client = new Client(HOST,PORT, "RESOLVE");
        clientThread = new ClientThread(client);
        clientThread.start();
    }
}
