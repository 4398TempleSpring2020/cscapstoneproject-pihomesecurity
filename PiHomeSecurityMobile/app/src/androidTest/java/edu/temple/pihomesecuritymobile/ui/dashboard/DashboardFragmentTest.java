package edu.temple.pihomesecuritymobile.ui.dashboard;

import android.content.Context;
import android.content.SharedPreferences;

import androidx.test.rule.ActivityTestRule;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.mockito.Mockito;

import edu.temple.pihomesecuritymobile.MainActivity;
import edu.temple.pihomesecuritymobile.R;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.junit.Assert.*;
import static org.mockito.Matchers.anyInt;
import static org.mockito.Matchers.anyString;

public class DashboardFragmentTest {
    private String escalate;
    private String resolve;
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
        resolve = "RESOLVE";
        escalate = "ESCALATE";
        this.mockPrefs = Mockito.mock(SharedPreferences.class);
        this.context = Mockito.mock(Context.class);
        Mockito.when(context.getSharedPreferences(anyString(), anyInt())).thenReturn(mockPrefs);
        Mockito.when(mockPrefs.getString(getHomeID, "")).thenReturn(homeID);
        Mockito.when(mockPrefs.getString(getUsername, "")).thenReturn(username);

    }

    @Test
    public void testSharedPrefs() {
        // Click on the icon - we can find it by the r.Id.
        onView(withId(R.id.navigation_dashboard))
                .perform(click());
        String testHome = mockPrefs.getString(getHomeID, "");
        assertEquals(homeID, testHome);
        String testUsername = mockPrefs.getString(getUsername, "");
        assertEquals(username, testUsername);
    }

    @Test
    public void testButtons() {
        // Click on the icon - we can find it by the r.Id.
        onView(withId(R.id.navigation_dashboard))
                .perform(click());
        onView(withId(R.id.resolve)).check(matches(withText(resolve)));
        onView(withId(R.id.escalate)).check(matches(withText(escalate)));
        onView(withId(R.id.resolve)).perform(click());
        onView(withId(R.id.escalate)).perform(click());
    }

}
