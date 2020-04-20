import cv2
from camera_proc_help import facial_recognition

class CamProc():
    def test_cv(self):
        print(cv2.__version__)

    def isAnomaly(self, image_dict):
        users = image_dict['users']

        sampled = image_dict['sampled']
        isAnom, face_match = facial_recognition(sampled, users)

        return(isAnom, face_match)
