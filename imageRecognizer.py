import tensorflow as tf
import numpy as np
import cv2
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import pathlib
print(tf.__version__)

from tensorflow.keras.models import load_model

model = load_model('trolley3.h5')
model.summary()


class_names = ['0', '1', '2', '3', '4', '5', '6', '7']

img_height = 400
img_width = 400



def imageRecognizer(c1=100, c2=200, minPredictions=3, averageConfidence=80):
    cap=cv2.VideoCapture(0)
    timer=1
    confidence=0
    p_class=''
    predictionsPointer=-1
    f_predictions=[] #create an list to hold frame classes
    for i in range(minPredictions):
        f_predictions.append(None)
    
    confidences=[None]* (minPredictions)
    print (f_predictions)
    while True:
        timer=timer+1
        avg=0
        
                    
        
        ret, img=cap.read()
        img= cv2.resize(img, (600,600),interpolation=cv2.INTER_AREA)
        
        kernel = np.ones((3,3), dtype = "uint8")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges=cv2.Canny(gray, c1,c2)    
        #cv2.imshow("Canny" , edges)
       
        edges = cv2.dilate(edges, kernel, iterations = 2)
        #cv2.imshow("Dilated", edges)

        

        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        biggestArea=0
        biggestIndex=0
        for i,contour in enumerate(contours):
            area = cv2.contourArea(contour)
            
            if(area > biggestArea):
                biggestArea=area
                biggestIndex=i
        
                
        try:
            x,y,w,h = cv2.boundingRect(contours[biggestIndex])
        except:
            x,y,w,h =0,0,1,1

        img = cv2.rectangle(img, (x,y),(x+w,y+h),(0,0,255),2)
        frame=img[y:y+h, x:x+w]
        
        cv2.imshow("OG",img)
            
            

        k=cv2.waitKey(100) #this makes the system wait as timeout continues
        
        frame=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if (timer % 10==0):
            predictionsPointer= predictionsPointer + 1
            frame=cv2.resize(frame, (img_width,img_height),interpolation=cv2.INTER_AREA)
            img_array = tf.expand_dims(frame, 0)
            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])
            
            p_class=class_names[np.argmax(score)]
            confidence=(100*np.max(score))
            print("Pointer: " +str(predictionsPointer) + " Class: " + p_class + " Confidence:" + str(confidence))
            f_predictions[predictionsPointer] = p_class
            print(f_predictions)
            confidences[predictionsPointer] = confidence

            

        if predictionsPointer==minPredictions-1:
            
            ##check predictions
            for i in range(1,minPredictions-1):
                if f_predictions[i] != f_predictions[i-1]:
                    predictionsPointer=-1
            if predictionsPointer!=-1:
                avg= sum(confidences)/len(confidences)
                if (avg > averageConfidence):
                    break
                else:
                    predictionsPointer=-1
            
        if k & 0XFF== 27:
            break
    print("Predicted Class is:"+ p_class)
    
    cap.release()
    cv2.destroyAllWindows()

    return(p_class)

#imageRecognizer(c1 =50 , c2=200, minPredictions=4, averageConfidence=95)
