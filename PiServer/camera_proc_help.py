import cv2
from matplotlib import pyplot as plt
import numpy as np
import face_recognition
from s3_client import S3_Client
import pickle
import os

# Test that moves an image in xstart:xend ystart:yend to the top left corner of the picture
def get_image(image_path, xstart, xend, ystart, yend):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    #img[400:900, 550:950] = [255, 255, 255]
    charles_face = img[xstart:xend, ystart:yend]
    img[0:(xend-xstart), 0:(yend-ystart)] = charles_face
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def test_draw_on_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    cv2.line(img, (0,0), (150, 150), (0, 255, 0), 15)
    cv2.rectangle(img, (15, 25), (200,150), (0,255,0), 5)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Charles', (1000,700), font, 3, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def test_matlab_plot(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([]) #used to hide tick values on x and y axis
    plt.plot([200,300,400],[100,200,300], 'c', linewidth=5)
    plt.show()

def test_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
def test_threshold(image_path):
    img = cv2.imread(image_path)
    retval, threshold = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)
    
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval2, threshold2 = cv2.threshold(grayscaled, 12, 255, cv2.THRESH_BINARY)
    gaus = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    retvaal2, otsu = cv2.threshold(grayscaled, 125, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    cv2.imshow('original', img)
    cv2.imshow('threshold', threshold)
    cv2.imshow('threshold2', threshold2)
    #otsu and gaus thresholds seem to work best for facial detection
    cv2.imshow('gaus', gaus)
    cv2.imshow('otsu', otsu)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def color_filtering():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_pink = np.array([100,100,50])
        upper_pink = np.array([255,255,255])
        
        mask = cv2.inRange(hsv, lower_pink, upper_pink)
        res = cv2.bitwise_and(frame, frame, mask=mask)
            
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        mask = cv2.rotate(mask, cv2.ROTATE_180)
        res = cv2.rotate(res, cv2.ROTATE_180)
            
        kernel = np.ones((15,15), np.float32)/225
        #smoothed = cv2.filter2D(res, -1, kernel)
        blur = cv2.GaussianBlur(res, (15,15), 0)
        median = cv2.medianBlur(res, 15)

        cv2.imshow('frame', frame)
        #cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        #cv2.imshow('smoothed', smoothed)
        #cv2.imshow('blur', blur)
        cv2.imshow('median', median)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break;
    cv2.destroyAllWindows()
    cap.release()
    
def facial_detection():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        img = cv2.rotate(img, cv2.ROTATE_180)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+h]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey+eh), (0, 255, 0), 2)
        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k==27:
            break
    cap.release()
    cv2.destroyAllWindows()
    
def facial_recognition(image_path_list, face_list):
    isAnom = False
    face_rec = False
    
    # Load the jpg files into numpy arrays
    image_list = []
    unknown_image_list = []

    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about
    # the first encoding in each image, so I grab index 0.
    unknown_face_present = False
    print('Embedding unknown faces')
    unknown_encs = []
    # get each unknown as np
    
    for image_path in image_path_list:
        #img = cv2.imread(image_path)
        #img = cv2.rotate(img, cv2.ROTATE_180)
        unknown_image_list.append(face_recognition.load_image_file(image_path))

    for unknown_image in unknown_image_list:
        try:
            unknown_encs.append(face_recognition.face_encodings(unknown_image)[0])
            print('UNKNOWN FACE PRESENT')
            unknown_face_present = True
        except IndexError:
            # no faces present
            print("No unknown face in unknown image")

    # if no faces detected, return false false
    if not unknown_face_present:
        return(False, False)
    
    known_faces = []
    user_face_present = False
    print('Embedding known faces')

    # check if path to embedded file exists
    for face_file in face_list:
        print(face_file)
        face_path = face_file.split(".jpg")[0]
        face_path += "_emb.txt"
        print(face_path)
        if(os.path.exists(face_path)):
            print('We have seen this face before ' + face_path)

            user_face_present = True
            with open(face_path, "rb") as ffile:
                known_faces.append(pickle.load(ffile))
        else:
            print('We have not seen this face before' + face_path + " " + str(face_file))
            # get each face as np
            image = face_recognition.load_image_file(face_file)

            print('Image file loaded')
            try:
                cur_face = face_recognition.face_encodings(image)[0]
                known_faces.append(cur_face)
                print('Known Face Present')
                with open(face_path, "wb") as ffile:
                    pickle.dump(cur_face, ffile)

                user_face_present = True
            except IndexError:
                # no face present
                print("ERROR: Unable to detect any faces in user uploaded image")
    # if no user faces detected in uploaded images but a unknown face is present
    # return True False
    if not user_face_present:
        return(True, False)
    
    # results is an array of True/False telling if the unknown face
    #matched anyone in the known_faces array
    print('Performing face matching')

    results_list = []
    
    print("len of unknown_encs: ",len(unknown_encs))
    for unknown_face_encoding in unknown_encs:
        print("running through unknown_encs")
        print("len of known_faces: ",len(known_faces))
        print("known faces: ",known_faces)
        for face in known_faces:
            print("face shape: ",face.shape)
        print("len unknown_face_encoding",len(unknown_face_encoding))
        print("unknown_face_encoding.shape is ",unknown_face_encoding.shape)
        results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
        for result in results:
            if(result):
                print('user was recognized')
                # return true if user recognized
                return(False, True)        

    print('user was recognized')
                    
    # return that face is present, but not recognized
    return(True, False)
