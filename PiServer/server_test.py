from run_sensors import run_everything
import ast

'''
keys:
   bucket : bucket name
   instance_id : id of the instance
   microphone : list of microphone files on s3
   camera : list of camera files on s3
   ultrasonic : list of ultrasonic files on s3
   face_match_flag : flag to say if a face match occured
   wasAlert : flag to determine if anomaly was detected (if false, everything should be empty and nothing will be uploaded to s3
   trigger_sensor_type : list of sensors that detected an anomaly
'''
ret_dict = run_everything(123)
#ret_dict = ast.literal_eval("{'microphone': ['123/1585615830.5592604/microphone/audio.wav'], 'camera': ['123/1585615830.5592604/camera/image_0.jpg', '123/1585615830.5592604/camera/image_1.jpg', '123/1585615830.5592604/camera/image_2.jpg', '123/1585615830.5592604/camera/image_3.jpg', '123/1585615830.5592604/camera/image_4.jpg', '123/1585615830.5592604/camera/image_5.jpg', '123/1585615830.5592604/camera/image_6.jpg', '123/1585615830.5592604/camera/image_7.jpg', '123/1585615830.5592604/camera/image_8.jpg', '123/1585615830.5592604/camera/image_9.jpg'], 'ultrasonic': ['123/1585615830.5592604/ultrasonic/ultra.txt'], 'bucket': 'whateverworks', 'instance_id': '1585615830.5592604', 'face_match_flag': False, 'wasAlert': True, 'trigger_sensor_type': ['camera']}")
