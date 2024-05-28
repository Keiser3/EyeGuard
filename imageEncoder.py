import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("DatabaseKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://eyeguard-25473-default-rtdb.firebaseio.com/',
    'storageBucket':'eyeguard-25473.appspot.com'

    })

imageDirPath = 'Images'
imagePath = os.listdir(imageDirPath)
imageList = []
userIDs = []
for path in imagePath:
    imageList.append(cv2.imread(os.path.join(imageDirPath,path)))
    userIDs  += os.path.splitext(path)[0]
    print(userIDs)
    fileName =  f'{imageDirPath}/{path}' 
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
print(userIDs)
def encodeImages(images):
    encodeList = []
    for image in images:
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        encodedImage = face_recognition.face_encodings(image)[0]
        print(encodedImage)
        encodeList.append(encodedImage)
        
    return encodeList

print('Encoding started......')
EncodesList = encodeImages(imageList)
EncodeListWithIds = [EncodesList, userIDs]
print(EncodeListWithIds)
print('Encoding complete')

file = open('Encodings/EncodingFile.p','wb')
pickle.dump(EncodeListWithIds,file)
file.close()
print('encodings stored successfully')