package edu.temple.awsapi;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Request is a class that will be used to hold request related information needed for a POST request
 */
class Response {
    //stuff we care about in the response
    private int statusCode=0;
    private String message="";
    private JSONObject body;
    private JSONArray bodyarray;


    /**
     * Setter method for the status code
     * @param statusCode: the status code as an int
     */
    void setStatusCode(int statusCode) {
        this.statusCode = statusCode;
    }

    /**
     * Getter method for the status code
     * @return status code as an int
     */
    int getStatusCode() {
        return statusCode;
    }

    /**
     * Setter method for the message
     * @param message: message as a Sting
     */
    void setMessage(String message) {
        this.message = message;
    }

    /**
     * Getter method for the message
     * @return message as a Sting
     */
    String getMessage() {
        return message;
    }

    /**
     * Setter method for the JSON body
     * @param body: body of the POST as String
     */
    void setBody(String body) {
        try {
            if (body.equals("")) {
                return;
            }
            //Log.d("Before replace: ", "" + body);

            body = body.replaceAll("\'", "\"");

            body = body.replaceAll("\",\\s\"", ", \"");
            body = body.replaceAll(",\\s\"", "\",\"");

            body = body.replaceAll("\": ", ":");
            body = body.replaceAll(": \"", ":");
            body = body.replaceAll(":\"", ":");
            body = body.replaceAll("\":", ":");
            body = body.replaceAll(":", "\":\"");

            body = body.replaceAll("\"\\}", "}");
            body = body.replaceAll("\\}", "\"}");
            body = body.replaceAll("\\{\"", "{");
            body = body.replaceAll("\\{", "{\"");

            //Log.d("After replace: ", "" + body);

            body = fixDate(body);
            if (body.contains("},")) {
                //  token.replaceAll("");
                this.bodyarray = new JSONArray(body);
                //Log.d("JSONArray count: ", "" + bodyarray.length());
            } else {
                String token = body.substring(1, body.length()-1);
                //Log.d("After substring: ", "" + token);
                this.body = new JSONObject(token);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    /**
     * Getter method for the body JSON
     * @return body of the POST as JSONObject
     */
    JSONObject getBody() {
        if (this.body != null) {
            return this.body;
        } else {
            Log.d("Null body", "JSONObject is empty");
            return null;
        }
    }

    /**
     * Getter method for the body JSON
     * @return body of the POST as JSONArray
     */
    JSONArray getBodyArray() {
        if (this.bodyarray != null) {
            return this.bodyarray;
        } else {
            Log.d("Null array", "JSONArray is empty");
            return null;
        }
    }

    /**
     * Getter method for the body JSON
     * @return body of the POST as String
     */
    String getBodyString() {
        if (this.body != null) {
            return this.body.toString();
        } else if (this.bodyarray!=null) {
            return this.bodyarray.toString();
        } else {
            return "No body to show";
        }
    }

    /**
     * fixDate() fixes the issue from the python lambdas for datetime variables
     * @param body: the String to be fixed
     * @return the String with date fixed
     */
    String fixDate(String body) {
        String[] tokens = body.split("datetime.datetime");
        String newDate;
        String newBody = "";
        if (tokens.length <= 1 ) {
            return body;
        }
        for (int i = 1; i<tokens.length; i++) {
            //Log.d("date tokens before: ", "" + tokens[i]);
            String[] tokens_temp = tokens[i].split("\\)");
            String[] date_tokens = tokens_temp[0].split(", ");
            date_tokens[0] = date_tokens[0].substring(1);
            newDate = date_tokens[1] + "-" + date_tokens[2] + "-" + date_tokens[0];
            //Log.d("date: ", "" + newDate);
            tokens[i] = "";
            tokens[i] = newDate + tokens_temp[1];
            //Log.d("date added back: ", "" + tokens[i]);

        }
        newBody += tokens[0];
        for (int i = 1; i<tokens.length; i++) {
            newBody += tokens[i];
        }

        //Log.d("After date fix: ", "" + newBody);
        return newBody;
    }
}
