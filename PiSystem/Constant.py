class Constant:
    #message types
    AlertMessage = "alert_message"
    Arm_MESSAGE = "arm_message"
    CONFIGURE_SETTINGS_MESSAGE = "configure_settings_message"
    PROFILE_UPDATE_MESSAGE = "profile_update_message"
    RESPONSE_MESSAGE = "response_message"

    #alert types
    FACE_RECOGNIZED_ALERT = "face_recognized_alert"
    FACE_NOT_RECOGNIZED_ALERT = "face_not_recognized_alert"

    #update types
    PROFILE_ADD_NEW_MEMBER = "add_new_member"
    PROFILE_ADD_MEMBER_FACE = "add_member_face"
    PROFILE_ADD_MY_FACE = "add_my_face"
    PROFILE_REMOVE_MEMBER = "remove_member"

    # Database connection
    host = "my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com"
    host_ip = "3.16.163.252"
    uname = "pi_user"
    password = "totallysecurepw!"
    db_name = "mypidb"

    # Pi server
    ACCOUNT_ID = 4
    port = 5001