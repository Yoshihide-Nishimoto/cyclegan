import cv2 
import glob

import os
facePath = cv2.CascadeClassifier("./cascade.xml")

def faceExtractor(file):
    img = cv2.imread(file)
    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = facePath.detectMultiScale(gray, 1.3, 5)
    if len(face)==0:
        print('faceExtractor :', 'not detect')
        return None

    for(x, y, w, h) in face:
        cropped = img[y: y+h, x: x+w]
    
    return cropped


files = glob.glob("./googleImages/*")
for file in files:
    face = faceExtractor(file)
    if face is not None:
        filename = os.path.basename(file)
        cv2.imwrite("./faceImages/"+filename, face)
    else:
        print("nonoooooo")
