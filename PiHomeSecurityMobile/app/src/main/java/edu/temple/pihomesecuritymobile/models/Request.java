package edu.temple.pihomesecuritymobile.models;

import org.json.JSONObject;

/**
 * Request is a class that will be used to hold request related information needed for a POST request
 */
public class Request {
    private String url;
    private String method;
    private JSONObject body = new JSONObject();

    /**
     * Setter method for the url
     * @param url: the url as a String
     */
    public void setUrl(String url) {
        this.url = url;
    }

    /**
     * Getter method for the url
     * @return url as a String
     */
    public String getUrl() {
        return url;
    }

    /**
     * Setter method for the method type
     * @param method: method type as a Sting
     */
    public void setMethod(String method) {
        this.method = method;
    }

    /**
     * Getter method for the method type
     * @return method type as a Sting
     */
    public String getMethod() {
        return method;
    }

    /**
     * Setter method for the JSON body
     * @param body: body of the POST as JSONObject
     */
    public void setBody(JSONObject body) {
        this.body = body;
    }

    /**
     * Getter method for the body JSON
     * @return body of the POST as JSONObject
     */
    public JSONObject getBody() {
        return this.body;
    }
}
