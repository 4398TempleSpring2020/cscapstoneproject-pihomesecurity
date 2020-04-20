

public interface Imessage {


    /**
     *
     * @return
     */
	
	String getData();
	
	void setData(JSONObject);
	
    /**
     *
     * @return
     */
    String getMessageType();
	
    /**
     *
     * @param messageType
     */
    void setMessageType(String messageType);
}
