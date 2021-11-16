import cv2
import os 
import numpy as np
import time

def get_model(method , facesData , labels):

    if method == 'LBPH' : emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()

    print('Training ('+method+')...')
    start = time.time()
    emotion_recognizer.train(facesData, np.array(labels))
    Training_time = time.time() - start
    print('Tiempo de entrenamiento ('+method+'): ', Training_time)

    emotion_recognizer.write('modelo'+method+'.xml')

dataPath = 'E:\Emotion_Recognition\Data'
emotionList = os.listdir(dataPath) #returns a list containing the names of the entries in the directory given by path
print('person list ' , emotionList)

labels = []
facesData = []
label = 0

for nameDir in emotionList:
    emotionPath = dataPath + '/' + nameDir
    print('Reading pictures')

    for fileName in os.listdir(emotionPath):
        print('Faces: ' , nameDir + '/' + fileName)
        labels.append(label)
        facesData.append(cv2.imread(emotionPath + '/' + fileName,0))

    label = label + 1

get_model('LBPH' , facesData , labels)
