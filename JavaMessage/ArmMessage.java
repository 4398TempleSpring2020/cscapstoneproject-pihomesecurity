

public class ArmMessage extends Message implements Imessage{
    
    String armMessage = "ARM_MESSAGE";
    
    String messageType;
    String armType;
    JSONObject messageData;
    
    /**
     * ArmMessage creation from parameter for only armType 
     * message type must be armMessage so assigns into field
     *
     * Creates a JSON object from messageType and armType
     * and stores into messageData
     * 
     * @param armType
     */
    public ArmMessage(String armType){
        this.messageType = armMessage;
        this.armType = armType;
        messageData = new JSONObject();
        messageData.put("messageType", messageType);
        messageData.put("armType", armType);
    }
    
    /**
     * GetData on any message returns the JSON object of the message
     * 
     * @return
     */
    @Override
    public JSONObject getData() {
        return messageData;
    }

    /**
     * Attempt to setData on an ArmMessage object checks that the JSON 
     * contains correct message type (armMessage) before setting the armType
     * from the JSON data.
     * 
     * @param armMsgData
     */
    @Override
    public void setData(JSONObject armMsgData) {
        String temp  = armMsgData.messageType;
        if (temp.equals(armMessage)){
            armType = armMsgData.armType;
        }
    }

    /**
     * Getter
     * 
     * @return
     */
    @Override
    public String getMessageType() {
        return messageType;
    }

    /**
     * Setter should set message type 
     * but only if is correct for this class of message 
     * 
     * @param messageType
     */
    @Override
    public void setMessageType(String messageType) {
        try {
            if(messageType.equals(armType)){
                this.messageType = messageType;
            }
        } catch (Exception e) {
        }
    }
        
    /**
     * Allows for setting armType to zero or one
     * the only permitted values
     * 
     * @param armType
     */
    public void setArmType(String armType){
        try {
            if((armType.equals("0"))||(armType.equals("1"))){
                this.armType = armType;
            }
        } catch (Exception e) {
        }
    }

    /**
     *  Getter
     * 
     * @return
     */
    public String getArmType() {
        return armType;
    }
    
}
