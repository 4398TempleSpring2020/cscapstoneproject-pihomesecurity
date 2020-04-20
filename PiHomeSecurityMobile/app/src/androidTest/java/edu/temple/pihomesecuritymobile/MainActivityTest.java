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

public class MainActivityTest {
    private String homeID;
    private String getHomeID;
    private String username;
    private String getUsername;

    SharedPreferences mockPrefs;
    Context context;

    @Rule
    public ActivityTestRule<MainActivity> activityTestRule = new ActivityTestRule<>(MainActivity.class);

    @Before
    public void before() throws Exception {
        homeID = "11";
        username = "danielle";
        getUsername = "UserName";
        getHomeID = "HomeID";
        this.mockPrefs = Mockito.mock(SharedPreferences.class);
        this.context = Mockito.mock(Context.class);
        Mockito.when(context.getSharedPreferences(anyString(), anyInt())).thenReturn(mockPrefs);
        Mockito.when(mockPrefs.getString(getHomeID, "")).thenReturn(homeID);
        Mockito.when(mockPrefs.getString(getUsername, "")).thenReturn(username);

    }

    @Test
    public void testSharedPrefs() {
        String testHome = mockPrefs.getString(getHomeID, "");
        assertEquals(homeID, testHome);
        String testUsername = mockPrefs.getString(getUsername, "");
        assertEquals(username, testUsername);
    }
}