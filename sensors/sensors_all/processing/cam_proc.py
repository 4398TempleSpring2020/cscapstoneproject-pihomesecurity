import cv2
from matplotlib import pyplot as plt
import numpy as np
import face_recognition

#This line of code adds a grayscale filter to the image
#img = cv2.imread('../data/cam/luke/image_18.jpg', cv2.IMREAD_GRAYSCALE)
class CamProc():
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

    def facial_recognition(image_path):
        # Load the jpg files into numpy arrays
        charles_image = face_recognition.load_image_file("known_people/charles.jpg")
        luke_image = face_recognition.load_image_file("known_people/luke.jpg")
        cat_image = face_recognition.load_image_file("known_people/cat.jpg")
        unknown_image = face_recognition.load_image_file(image_path)

        # Get the face encodings for each face in each image file
        # Since there could be more than one face in each image, it returns a list of encodings.
        # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
        try:
            charles_face_encoding = face_recognition.face_encodings(charles_image)[0]
            luke_face_encoding = face_recognition.face_encodings(luke_image)[0]
            cat_face_encoding = face_recognition.face_encodings(cat_image)[0]
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            quit()

        known_faces = [
            charles_face_encoding,
            luke_face_encoding,
            cat_face_encoding
        ]

        # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
        results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

        print("Is the unknown face a picture of Charles? {}".format(results[0]))
        print("Is the unknown face a picture of Luke? {}".format(results[1]))
        print("Is the unknown face a picture of Cat's daughter? {}".format(results[2]))
        print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
        
        for i in range(0, len(known_faces)):
            if(results[i] == True):
                return True
            #print(results[i])
        return False

# CamProc.get_image('../data/cam/charles/charles_5.jpg', 400, 900, 550, 950)
# CamProc.test_draw_on_image('../data/cam/charles/charles_5.jpg')
# CamProc.test_matlab_plot('../data/cam/charles/charles_5.jpg')
# CamProc.test_video()
# CamProc.test_threshold('../data/cam/charles/charles_5.jpg')
# CamProc.color_filtering()
print(CamProc.facial_recognition("unknown_people/unknown1.jpg"))
print(CamProc.facial_recognition("unknown_people/unknown2.jpg"))
print(CamProc.facial_recognition("unknown_people/unknown3.jpg"))
print(CamProc.facial_recognition("unknown_people/unknown4.jpg"))
