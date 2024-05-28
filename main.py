import cv2
import os
import pickle
import face_recognition
import numpy 
import cvzone
import firebase_admin
from datetime import datetime
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("DatabaseKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://eyeguard-25473-default-rtdb.firebaseio.com/',
    'storageBucket':'eyeguard-25473.appspot.com'
    })
bucket = storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
imageBackground = cv2.imread('Ressources/background2.png')
userImage= []
modeDirPath = 'Ressources/modes'
modePath = os.listdir(modeDirPath)
modeList = []
for path in modePath:
    modeList.append(cv2.imread(os.path.join(modeDirPath,path)))


print('loading Encodes File......')
file = open('Encodings/EncodingFile.p','rb+')
encodeListWithIds = pickle.load(file)
file.close()
print(encodeListWithIds)
encodesList, userIds = encodeListWithIds
print(userIds)
print("Encodes File Loaded successfully!")

mode = 0
cnt = 0
id = -1

while True:
    success, image = cap.read()

    smallImage = cv2.resize(image,(0,0),None,0.25,0.25)
    smallImage = cv2.cvtColor(smallImage, cv2.COLOR_BGR2RGB)
    
    faceCurrFrame = face_recognition.face_locations(smallImage)
    encodeCurrFrame = face_recognition.face_encodings(smallImage,faceCurrFrame)
    

    imageBackground[196:196+480,78:78+640] = image
    imageBackground[44:44+633,808:808+414] = modeList[mode]

    for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
        matches = face_recognition.compare_faces(encodesList,encodeFace)
        faceDist = face_recognition.face_distance(encodesList,encodeFace)
        matchIndex = numpy.argmin(faceDist)
        if matches[matchIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4 , x2*4, y2*4, x1*4
            bbox = 73+x1, 188+y1, x2-x1, y2 -y1
            imageBackground = cvzone.cornerRect(imageBackground,bbox,rt=0)
            id = userIds[matchIndex]
            if cnt ==0:
                cnt = 1
                mode = 1
    if cnt != 0:

        if cnt ==1:
            userInfo = db.reference(f'Students/{id}').get()
            blob = bucket.get_blob(f'Images/{id}.jpg')
            array = numpy.frombuffer(blob.download_as_string(), numpy.uint8)
            userImage = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
            ref = db.reference(f'Students/{id}')
            userInfo['last_seen'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            ref.child('last_seen').set(userInfo['last_seen'])
        if 10<cnt<20:
            mode = 2
        imageBackground[44:44+633,808:808+414] = modeList[mode]    
        if cnt <=10:
           cv2.putText(imageBackground,str(userInfo['name']),(808,445),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
           cv2.putText(imageBackground,str(userInfo['filliere']),(1006,493),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
           imageBackground[175:175+216, 909:909+216] = userImage
        cnt +=1
        if cnt>=20:
            cnt = 0
            mode = 0
            userInfo = []
            userImage = []
            imageBackground[44:44+633,808:808+414] = modeList[mode]
    cv2.imshow("EyeGuard",imageBackground)
    cv2.waitKey(1)