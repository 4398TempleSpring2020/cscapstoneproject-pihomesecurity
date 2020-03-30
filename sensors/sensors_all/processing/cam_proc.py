import cv2
from matplotlib import pyplot as plt
import numpy as np

#This line of code adds a grayscale filter to the image
#img = cv2.imread('../data/cam/luke/image_18.jpg', cv2.IMREAD_GRAYSCALE)

img = cv2.imread('../data/cam/charles/charles_5.jpg', cv2.IMREAD_COLOR)
#img[400:900, 550:950] = [255, 255, 255]

charles_face = img[400:900, 550:950]
img[0:500, 0:400] = charles_face
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
cv2.line(img, (0,0), (150, 150), (0, 255, 0), 15)
cv2.rectangle(img, (15, 25), (200,150), (0,255,0), 5)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'Charles', (1000,700), font, 3, (255, 0, 0), 2, cv2.LINE_AA)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

"""
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(cv2.__version__)
"""

"""
This code just draws stuff using matlaplot
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([]) #used to hide tick values on x and y axis
plt.plot([200,300,400],[100,200,300], 'c', linewidth=5)
plt.show()

"""

"""
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
"""
