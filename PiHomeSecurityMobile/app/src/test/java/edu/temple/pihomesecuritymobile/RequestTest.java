package edu.temple.pihomesecuritymobile;

import org.json.JSONException;
import org.json.JSONObject;
import org.junit.Test;

import edu.temple.pihomesecuritymobile.models.Request;

import static org.junit.Assert.assertEquals;

public class RequestTest {
    private Request request = new Request();
    @Test
    public void setUrlEqualsGetUrl() {
        String test_url="https://www.temple.edu";
        request.setUrl(test_url);
        assertEquals(test_url, request.getUrl());
    }

    @Test
    public void setMethodEqualsGetMethod() {
        String test_method="POST";
        request.setMethod(test_method);
        assertEquals(test_method, request.getMethod());
    }

    @Test
    public void setBodyEqualsGetBody() {
        JSONObject jsonObject = new JSONObject();
        String test_key1 = "key1";
        String test_key2 = "key2";
        String param_1 = "param1";
        String param_2 = "param2";
        try {
            jsonObject.put(test_key1, param_1);
            jsonObject.put(test_key2, param_2);

            request.setBody(jsonObject);
            JSONObject result = request.getBody();
            assertEquals(jsonObject.length(), result.length());
            assertEquals(jsonObject.getString(test_key1), result.getString(test_key1));
            assertEquals(jsonObject.getString(test_key2), result.getString(test_key2));
            assertEquals(jsonObject.toString(), result.toString());

        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

}