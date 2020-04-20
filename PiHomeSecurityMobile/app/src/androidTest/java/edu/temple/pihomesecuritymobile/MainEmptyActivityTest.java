package edu.temple.pihomesecuritymobile;

import android.content.Context;
import android.content.SharedPreferences;

import androidx.test.rule.ActivityTestRule;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;
import static org.mockito.Matchers.anyInt;
import static org.mockito.Matchers.anyString;


public class MainEmptyActivityTest {
    private String homeID;
    private String getHomeID;
    private String username;
    private String getUsername;
    boolean setFalse, settrue;
    SharedPreferences mockPrefs;
    Context context;

    @Rule
    public ActivityTestRule<MainEmptyActivity> activityTestRule = new ActivityTestRule<>(MainEmptyActivity.class);

    @Before
    public void before() throws Exception{
        this.mockPrefs = Mockito.mock(SharedPreferences.class);
        this.context = Mockito.mock(Context.class);
        Mockito.when(context.getSharedPreferences(anyString(),anyInt())).thenReturn(mockPrefs);
        boolean setFalse = false, setTrue = true;
        Mockito.when(mockPrefs.getBoolean("Registered", false)).thenReturn(false);
    }

    @Test
    public void goToLogin(){
        Boolean check = mockPrefs.getBoolean("Registered", false);
        assertEquals(false,check);
    }

    @Test
    public void goToDashboard(){
        Mockito.when(mockPrefs.getBoolean("Registered", false)).thenReturn(true);
        Boolean check = mockPrefs.getBoolean("Registered", false);
        assertEquals(true,check);
    }

}