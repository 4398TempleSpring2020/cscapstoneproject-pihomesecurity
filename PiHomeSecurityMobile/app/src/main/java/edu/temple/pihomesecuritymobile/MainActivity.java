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
        client = new Client(null,0);
        clientThread = new ClientThread(client);
        clientThread.start();
        sharePrefs = getSharedPreferences("PREF_NAME",MODE_PRIVATE);
        if(formBundle != null){
            String form[] = formBundle.getStringArray("form");
            sharePrefs.edit().putString("HomeID",form[0]).apply();
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

    @Override
    public void soundAlarm() {
        JSONObject message = new JSONObject();
        try {
            message.put("Message", "alert_message");
            message.put("AlarmSetting",1);
            client.send(message);
        } catch (JSONException e){
            Log.e("SENDING ALARM MESSAGE", e.toString());
        }
        Toast.makeText(getApplicationContext(),"Sounding Alarm", Toast.LENGTH_SHORT).show();
    }


}
