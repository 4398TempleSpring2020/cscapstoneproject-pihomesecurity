package edu.temple.pihomesecuritymobile;

import android.os.Bundle;
import android.widget.Toast;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import edu.temple.pihomesecuritymobile.ui.dashboard.DashboardFragment;
import edu.temple.pihomesecuritymobile.ui.home.HomeFragment;
import edu.temple.pihomesecuritymobile.ui.notifications.NotificationsFragment;

public class MainActivity extends AppCompatActivity implements HomeFragment.soundButtonListener, DashboardFragment.onFragListener, NotificationsFragment.onFragListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        BottomNavigationView navView = findViewById(R.id.nav_view);
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
        Toast.makeText(getApplicationContext(),"Sounding Alarm", Toast.LENGTH_SHORT).show();
    }
}
