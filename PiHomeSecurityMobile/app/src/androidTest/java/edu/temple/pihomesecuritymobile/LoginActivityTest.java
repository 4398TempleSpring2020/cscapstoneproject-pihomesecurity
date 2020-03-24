package edu.temple.pihomesecuritymobile;

import androidx.test.filters.LargeTest;
import androidx.test.rule.ActivityTestRule;
import androidx.test.runner.AndroidJUnit4;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.closeSoftKeyboard;
import static androidx.test.espresso.action.ViewActions.typeText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.hasErrorText;
import static androidx.test.espresso.matcher.ViewMatchers.withId;

@RunWith(AndroidJUnit4.class)
@LargeTest
public class LoginActivityTest {
    private String emptyString;
    private String spaceString;
    private String validWords;
    private String emptyError;
    private String userError;
    private String validUsername;
    private String validPassword;

    @Rule
    public ActivityTestRule<LoginActivity> activityRule = new ActivityTestRule<>(LoginActivity.class);

    @Before
    public void initStrings() {
        emptyString = "";
        spaceString = " ";
        validPassword = "1234";
        validUsername = "danielle";
        validWords = "Temple";
        emptyError = "Field is empty";
        userError = "Incorrect password or username";
    }

    @Test
    public void testEmptyStrings() {
        onView(withId(R.id.editText)).perform(typeText(emptyString), closeSoftKeyboard());
        onView(withId(R.id.editText2)).perform(typeText(emptyString), closeSoftKeyboard());

        onView(withId(R.id.button)).perform(click());

        onView(withId(R.id.editText)).check(matches(hasErrorText(emptyError)));
        onView(withId(R.id.editText2)).check(matches(hasErrorText(emptyError)));
    }

    @Test
    public void testWhiteSpaceStrings() {
        onView(withId(R.id.editText)).perform(typeText(spaceString), closeSoftKeyboard());
        onView(withId(R.id.editText2)).perform(typeText(spaceString), closeSoftKeyboard());

        onView(withId(R.id.button)).perform(click());

        onView(withId(R.id.editText)).check(matches(hasErrorText(emptyError)));
        onView(withId(R.id.editText2)).check(matches(hasErrorText(emptyError)));
    }

    @Test
    public void testWrongUsername() {
        onView(withId(R.id.editText)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText2)).perform(typeText(validWords), closeSoftKeyboard());

        onView(withId(R.id.button)).perform(click());

        onView(withId(R.id.editText)).check(matches(hasErrorText(userError)));
        onView(withId(R.id.editText2)).check(matches(hasErrorText(userError)));
    }

    @Test
    public void testWrongPassword() {
        onView(withId(R.id.editText)).perform(typeText(validUsername), closeSoftKeyboard());
        onView(withId(R.id.editText2)).perform(typeText(validWords), closeSoftKeyboard());

        onView(withId(R.id.button)).perform(click());

        onView(withId(R.id.editText)).check(matches(hasErrorText(userError)));
        onView(withId(R.id.editText2)).check(matches(hasErrorText(userError)));
    }
}