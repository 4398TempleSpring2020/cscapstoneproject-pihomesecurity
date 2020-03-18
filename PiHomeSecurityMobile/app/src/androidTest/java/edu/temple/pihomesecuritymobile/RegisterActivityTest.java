package edu.temple.pihomesecuritymobile;

import androidx.test.filters.LargeTest;
import androidx.test.runner.AndroidJUnit4;
import androidx.test.rule.ActivityTestRule;

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
public class RegisterActivityTest {

    private String emptyString;
    private String spaceString;
    private String validWords;
    private String passwordDiff;
    private String validPhone;
    private String emptyErrorText;
    private String passwordErrorText;
    private String phoneNumErrorText;
    private String validAddress;
    private String validPin;
    private String tenWord;
    private String homeAddrError;
    private String pinError;
    private String duplicateError;
    private String duplicateUsername;

    @Rule
    public ActivityTestRule<RegisterActivity> activityRule = new ActivityTestRule<>(RegisterActivity.class);

    @Before
    public void initStrings() {
        emptyString = "";
        spaceString = " ";
        validWords = "Temple";
        validPhone = "2151234567";
        passwordDiff = "diffpassword";
        emptyErrorText = "Field is empty";
        passwordErrorText = "Passwords do not match";
        validAddress = "1801 N Broad St";
        validPin = "1234";
        phoneNumErrorText = "Please enter a phone number like 1231231234";
        tenWord = "aaaaaaaaaa";
        homeAddrError = "Home address not found";
        pinError = "Pin does not match";
        duplicateError = "Username exists";
        duplicateUsername = "danielle";
    }

    @Test
    public void testEmptyStrings() {
        onView(withId(R.id.editText4)).perform(typeText(emptyString), closeSoftKeyboard());
        onView(withId(R.id.editText3)).perform(typeText(emptyString), closeSoftKeyboard());
        onView(withId(R.id.editText5)).perform(typeText(emptyString), closeSoftKeyboard());
        onView(withId(R.id.editText6)).perform(typeText(emptyString), closeSoftKeyboard());
        onView(withId(R.id.pinText)).perform(typeText(emptyString), closeSoftKeyboard());
        onView(withId(R.id.phoneNumText)).perform(typeText(emptyString), closeSoftKeyboard());

        onView(withId(R.id.registerButton)).perform(click());

        onView(withId(R.id.editText4)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.editText3)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.editText5)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.editText6)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.pinText)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.phoneNumText)).check(matches(hasErrorText(emptyErrorText)));
    }

    @Test
    public void testWhiteSpaceStrings() {
        onView(withId(R.id.editText4)).perform(typeText(spaceString), closeSoftKeyboard());
        onView(withId(R.id.editText3)).perform(typeText(spaceString), closeSoftKeyboard());
        onView(withId(R.id.editText5)).perform(typeText(spaceString), closeSoftKeyboard());
        onView(withId(R.id.editText6)).perform(typeText(spaceString), closeSoftKeyboard());
        onView(withId(R.id.pinText)).perform(typeText(spaceString), closeSoftKeyboard());
        onView(withId(R.id.phoneNumText)).perform(typeText(spaceString), closeSoftKeyboard());

        onView(withId(R.id.registerButton)).perform(click());

        onView(withId(R.id.editText4)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.editText3)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.editText5)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.editText6)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.pinText)).check(matches(hasErrorText(emptyErrorText)));
        onView(withId(R.id.phoneNumText)).check(matches(hasErrorText(emptyErrorText)));
    }

    @Test
    public void testPasswordStrings() {
        onView(withId(R.id.editText4)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText3)).perform(typeText(validAddress), closeSoftKeyboard());
        onView(withId(R.id.editText5)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText6)).perform(typeText(passwordDiff), closeSoftKeyboard());
        onView(withId(R.id.pinText)).perform(typeText(validPin), closeSoftKeyboard());
        onView(withId(R.id.phoneNumText)).perform(typeText(validPhone), closeSoftKeyboard());

        onView(withId(R.id.registerButton)).perform(click());

        // Check the error text
        onView(withId(R.id.editText5)).check(matches(hasErrorText(passwordErrorText)));
        onView(withId(R.id.editText6)).check(matches(hasErrorText(passwordErrorText)));
    }

    @Test
    public void testPhoneNumberLength() {
        onView(withId(R.id.editText4)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText3)).perform(typeText(validAddress), closeSoftKeyboard());
        onView(withId(R.id.editText5)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText6)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.pinText)).perform(typeText(validPin), closeSoftKeyboard());
        onView(withId(R.id.phoneNumText)).perform(typeText(validWords), closeSoftKeyboard());

        onView(withId(R.id.registerButton)).perform(click());

        onView(withId(R.id.phoneNumText)).check(matches(hasErrorText(phoneNumErrorText)));
    }

    @Test
    public void testPhoneNumberValid() {
        // Type text and then press the button.
        onView(withId(R.id.editText4)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText3)).perform(typeText(validAddress), closeSoftKeyboard());
        onView(withId(R.id.editText5)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText6)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.pinText)).perform(typeText(validPin), closeSoftKeyboard());
        onView(withId(R.id.phoneNumText)).perform(typeText(tenWord), closeSoftKeyboard());

        onView(withId(R.id.registerButton)).perform(click());

        onView(withId(R.id.phoneNumText)).check(matches(hasErrorText(phoneNumErrorText)));
    }

    @Test
    public void testAddress() {
        onView(withId(R.id.editText4)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText3)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText5)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText6)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.pinText)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.phoneNumText)).perform(typeText(validPhone), closeSoftKeyboard());

        onView(withId(R.id.registerButton)).perform(click());

        onView(withId(R.id.editText3)).check(matches(hasErrorText(homeAddrError)));
    }

    @Test
    public void testPin() {
        onView(withId(R.id.editText4)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText3)).perform(typeText(validAddress), closeSoftKeyboard());
        onView(withId(R.id.editText5)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText6)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.pinText)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.phoneNumText)).perform(typeText(validPhone), closeSoftKeyboard());

        onView(withId(R.id.registerButton)).perform(click());

        onView(withId(R.id.pinText)).check(matches(hasErrorText(pinError)));
    }

    @Test
    public void testDuplicate() {
        onView(withId(R.id.editText4)).perform(typeText(duplicateUsername), closeSoftKeyboard());
        onView(withId(R.id.editText3)).perform(typeText(validAddress), closeSoftKeyboard());
        onView(withId(R.id.editText5)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.editText6)).perform(typeText(validWords), closeSoftKeyboard());
        onView(withId(R.id.pinText)).perform(typeText(validPin), closeSoftKeyboard());
        onView(withId(R.id.phoneNumText)).perform(typeText(validPhone), closeSoftKeyboard());

        onView(withId(R.id.registerButton)).perform(click());

        onView(withId(R.id.editText4)).check(matches(hasErrorText(duplicateError)));
    }

}