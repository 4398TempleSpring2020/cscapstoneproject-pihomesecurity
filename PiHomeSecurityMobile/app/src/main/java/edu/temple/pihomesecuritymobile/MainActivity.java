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
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        BottomNavigationView navView = findViewById(R.id.nav_view);
        Bundle formBundle = getIntent().getExtras();
        client = new Client("3.16.163.252",5001);
        clientThread = new ClientThread(client);
        clientThread.start();
        JSONObject json = new JSONObject();
        try{
            json.put("Pi_mobile","pi_mobile");
            client.send("Pi_mobile");
        } catch (Exception e){

        }
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
        JSONObject message = new JSONObject();
        try {
            message.put("message_type", "alert_message");
            message.put("alert_type","sound_alarm");
            //client.send(message);
            client.send("PANIC");
        } catch (JSONException e){
            Log.e("SENDING ALARM MESSAGE", e.toString());
        }
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
        JSONObject message = new JSONObject();
        try{
            message.put("message_type","arm_message");
            if(setFlag){
                message.put("arm_type",1);
                client.send("ARM");
            } else {
                message.put("arm_type",0);
                client.send("DISARM");
            }
        } catch (JSONException e){
            Log.e("SENDING ARM MESSAGE", e.toString());
        }
    }


    @Override
    public void escalateRsp(JSONObject msg) {
        client.send("ESCALATE");
        //client.send(msg);
    }

    @Override
    public void resolveRsp(JSONObject msg) {
        client.send("RESOLVE");
        //client.send(msg);
    }
}
