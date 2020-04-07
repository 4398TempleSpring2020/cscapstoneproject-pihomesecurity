package edu.temple.pihomesecuritymobile;

import android.content.Intent;

import androidx.test.rule.ActivityTestRule;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.RootMatchers.isDialog;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.junit.Assert.*;

public class ImageViewerTest {
    private String title;
    private String confirm;
    private String cancel;
    private String homeID;
    private String[] imagePaths;
    private String safeBut;
    private String downBut;
    private String backBut;

    @Before
    public void setUp() throws Exception {
        title="Confirm Action";
        confirm ="Upload to Pi";
        cancel = "Cancel";
        imagePaths = new String[]{"https://d1uydrbc3kb9ug.cloudfront.net/4/1585787849.1312783/camera/image_0.jpg"};
        homeID = "11";
        backBut = "Back";
        downBut = "Download";
        safeBut = "Upload as Safe";
    }

    @Rule
    public ActivityTestRule<ImageViewer> activityRule = new ActivityTestRule<>(ImageViewer.class,true, false);

    @Test
    public void checkDialog() {
        Intent i = new Intent();
        i.putExtra("image_id", 0);
        i.putExtra("images", imagePaths);
        i.putExtra("home_id", homeID);
        activityRule.launchActivity(i);

        onView(withId(R.id.buttonDownload)).check(matches(withText(downBut)));
        onView(withId(R.id.buttonSafe)).check(matches(withText(safeBut)));
        onView(withId(R.id.buttonBack)).check(matches(withText(backBut)));

        onView(withId(R.id.buttonSafe)).perform(click());

        int titleId = activityRule.getActivity().getResources()
                .getIdentifier( "alertTitle", "id", "android" );

        onView(withId(titleId))
                .inRoot(isDialog())
                .check(matches(withText(title)))
                .check(matches(isDisplayed()));

        onView(withId(android.R.id.button3))
                .inRoot(isDialog())
                .check(matches(withText(confirm)))
                .check(matches(isDisplayed()));

        onView(withId(android.R.id.button1))
                .inRoot(isDialog())
                .check(matches(withText(cancel)))
                .check(matches(isDisplayed()));

        onView(withId(android.R.id.button1)).perform(click());

        onView(withId(R.id.buttonBack)).perform(click());

    }
}