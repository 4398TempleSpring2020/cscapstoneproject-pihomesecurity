package edu.temple.pihomesecuritymobile.ui.home;

import androidx.test.rule.ActivityTestRule;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;

import edu.temple.pihomesecuritymobile.MainActivity;
import edu.temple.pihomesecuritymobile.R;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isChecked;
import static androidx.test.espresso.matcher.ViewMatchers.isNotChecked;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;

public class HomeFragmentTest {
    private String arm;
    private String disarm;
    private String sound;

    @Rule
    public ActivityTestRule<MainActivity> activityTestRule = new ActivityTestRule<>(MainActivity.class);

    @Before
    public void before() throws Exception {
        sound = "Sound";
        arm = "Alarm: active";
        disarm = "Alarm: unactive";
    }

    @Test
    public void testFragment() {
        // Click on the icon - we can find it by the r.Id.
        onView(withId(R.id.navigation_home))
                .perform(click());
    }

    @Test
    public void testButtons() {
        // Click on the icon - we can find it by the r.Id.
        onView(withId(R.id.navigation_home))
                .perform(click());
        onView(withId(R.id.soundButtton)).check(matches(withText(sound)));

        onView(withId(R.id.alarmStr)).check(matches(withText(disarm)));
        onView(withId(R.id.alarmSwitch)).check(matches(isNotChecked()));
        onView(withId(R.id.alarmSwitch)).perform(click());

        onView(withId(R.id.alarmStr)).check(matches(withText(arm)));
        onView(withId(R.id.alarmSwitch)).check(matches(isChecked()));

        onView(withId(R.id.alarmSwitch)).perform(click());
        onView(withId(R.id.alarmStr)).check(matches(withText(disarm)));
        onView(withId(R.id.alarmSwitch)).check(matches(isNotChecked()));
    }

}
