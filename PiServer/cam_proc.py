import cv2
from camera_proc_help import facial_recognition

class CamProc():
    def test_cv(self):
        print(cv2.__version__)

    def isAnomaly(self, image_dict):
        users = image_dict['users']

        sampled = image_dict['sampled']
        isAnom = False
        face_match = False
        for file_a in sampled:
            # attempt to recognize faces
            isAnom_temp, face_rec_temp = facial_recognition(file_a, users)
            
            # per image anom detection
            if(isAnom_temp):
                isAnom = True
            if(face_rec_temp):
                face_match = True

            # end early if user face at all
            if(isAnom and face_match):
                break
        
        return(isAnom, face_match)
