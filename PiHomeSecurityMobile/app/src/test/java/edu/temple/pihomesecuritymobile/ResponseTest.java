package edu.temple.pihomesecuritymobile;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.junit.Test;

import edu.temple.pihomesecuritymobile.models.Response;

import static org.junit.Assert.assertEquals;

public class ResponseTest {
    private Response response = new Response();

    @Test
    public void setStatusCodeEqualsGetStatusCode() {
        int test_status = 101;
        response.setStatusCode(test_status);
        assertEquals(test_status, response.getStatusCode());
    }

    @Test
    public void setMessageEqualsGetMessage() {
        String test_message = "this is a test";
        response.setMessage(test_message);
        assertEquals(test_message, response.getMessage());
    }

    @Test
    public void setBodyArrayEqualsGetBodyArray() {
        JSONArray jsonArray = new JSONArray();
        JSONObject jsonObject1 = new JSONObject();
        JSONObject jsonObject2 = new JSONObject();
        String test_key1 = "key1";
        String test_key2 = "key2";
        String param_1 = "param1";
        String param_2 = "param2";
        String test_strings = "[{\"" + test_key1 + "\":\"" + param_1 + "\",\"" + test_key2 + "\":\"" + param_2 + "\"}, {\"" + test_key1 + "\":\"" + param_1 + "\",\"" + test_key2 + "\":\"" + param_2 + "\"}]";
        String test_strings2 = test_strings.replaceAll("\"", "'");
        try {
            jsonObject1.put(test_key1, param_1);
            jsonObject1.put(test_key2, param_2);
            jsonObject2.put(test_key1, param_1);
            jsonObject2.put(test_key2, param_2);
            jsonArray.put(jsonObject1);
            jsonArray.put(jsonObject2);
            response.setBody(test_strings);
            JSONArray json_result1 = response.getBodyArray();
            String result = response.getBodyString();
            assertEquals(jsonArray.length(), json_result1.length());
            assertEquals(jsonArray.get(0), json_result1.get(0));
            assertEquals(jsonArray.get(1), json_result1.get(1));
            assertEquals(jsonArray.toString(), result);

            response.setBody(test_strings2);
            JSONArray json_result2 = response.getBodyArray();
            result = response.getBodyString();
            assertEquals(jsonArray.length(), json_result2.length());
            assertEquals(jsonArray.get(0), json_result2.get(0));
            assertEquals(jsonArray.get(1), json_result2.get(1));
            assertEquals(jsonArray.toString(), result);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void setBodyEqualsGetBody() {
        JSONObject jsonObject1 = new JSONObject();
        String test_key1 = "key1";
        String test_key2 = "key2";
        String param_1 = "param1";
        String param_2 = "param2";
        String test_strings = "[{\"" + test_key1 + "\":\"" + param_1 + "\",\"" + test_key2 + "\":\"" + param_2 + "\"}]";
        String test_strings2 = test_strings.replaceAll("\"", "'");

        try {
            jsonObject1.put(test_key1, param_1);
            jsonObject1.put(test_key2, param_2);
            response.setBody(test_strings);
            JSONObject json_result1 = response.getBody();
            String result = response.getBodyString();
            assertEquals(jsonObject1.length(), json_result1.length());
            assertEquals(jsonObject1.getString(test_key1), json_result1.getString(test_key1));
            assertEquals(jsonObject1.getString(test_key2), json_result1.getString(test_key2));
            assertEquals(jsonObject1.toString(), result);

            response.setBody(test_strings2);
            JSONObject json_result2 = response.getBody();
            result = response.getBodyString();
            assertEquals(jsonObject1.length(), json_result2.length());
            assertEquals(jsonObject1.getString(test_key1), json_result2.getString(test_key1));
            assertEquals(jsonObject1.getString(test_key2), json_result2.getString(test_key2));
            assertEquals(jsonObject1.toString(), result);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testDateCorrect() {
        String date = "\"datetime.datetime(2020, 3, 11, 20, 5, 41)\"";
        String correct_date = "\"3-11-2020\"";
        assertEquals(correct_date, response.fixDate(date));

        String date2 = "{\"LastLogin\":\"datetime.datetime(2020, 3, 11, 20, 5, 41)\"}, {\"LastLogin\":\"datetime.datetime(2020, 03, 06, 26, 10, 41)\"}";
        String correct_date2 = "{\"LastLogin\":\"3-11-2020\"}, {\"LastLogin\":\"03-06-2020\"}";
        assertEquals(correct_date2, response.fixDate(date2));
    }
}