package edu.temple.pihomesecuritymobile.ui.notifications;

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
import static androidx.test.espresso.action.ViewActions.pressBack;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.RootMatchers.isDialog;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.junit.Assert.*;
import static org.mockito.Matchers.anyInt;
import static org.mockito.Matchers.anyString;

public class NotificationsFragmentTest {
    private String title;
    private String camera;
    private String gallery;
    private String homeID;
    private String getHomeID;
    private String uploadBut;

    SharedPreferences mockPrefs;
    Context context;

    @Rule
    public ActivityTestRule<MainActivity> activityTestRule = new ActivityTestRule<>(MainActivity.class);

    @Before
    public void before() throws Exception {
        homeID = "11";
        getHomeID = "HomeID";
        uploadBut = "Upload Photo to Raspberry Pi";
        title = "Photo Upload";
        camera = "Camera";
        gallery = "Gallery";
        this.mockPrefs = Mockito.mock(SharedPreferences.class);
        this.context = Mockito.mock(Context.class);
        Mockito.when(context.getSharedPreferences(anyString(), anyInt())).thenReturn(mockPrefs);
        Mockito.when(mockPrefs.getString(getHomeID, "")).thenReturn(homeID);

    }

    @Test
    public void testSharedPrefs() {
        // Click on the icon - we can find it by the r.Id.
        onView(withId(R.id.navigation_notifications))
                .perform(click());
        String testHome = mockPrefs.getString(getHomeID, "");
        assertEquals(homeID, testHome);
    }

    @Test
    public void testUploadPhotoButton() {
        // Click on the icon - we can find it by the r.Id.
        onView(withId(R.id.navigation_notifications))
                .perform(click());
        onView(withId(R.id.buttonPhotos)).check(matches(withText(uploadBut)));
        onView(withId(R.id.buttonPhotos)).perform(click());
        int titleId = activityTestRule.getActivity().getResources()
                .getIdentifier("alertTitle", "id", "android");
        onView(withId(titleId))
                .inRoot(isDialog())
                .check(matches(withText(title)))
                .check(matches(isDisplayed()));
        onView(withId(android.R.id.button2))
                .inRoot(isDialog())
                .check(matches(withText(gallery)))
                .check(matches(isDisplayed()));
        onView(withId(android.R.id.button1))
                .inRoot(isDialog())
                .check(matches(withText(camera)))
                .check(matches(isDisplayed()));
        onView(withId(titleId)).perform(pressBack());
    }
}