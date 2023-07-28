import cv2
import face_recognition
import pickle
import os

folderPath = "images" # folder which contains all the image folders of each person for training
studentImageFolders = os.listdir(folderPath)
studentsImageList = []
student_names = []
for path in studentImageFolders:
    studPath = folderPath+"/"+path
    studentImages = os.listdir(studPath)
    student_names.append(path)
    stud = []
    for imagePath in studentImages:
        stud.append(cv2.imread(os.path.join(studPath,imagePath)))
    studentsImageList.append(stud)
print(len(studentsImageList))


def findEncodings(folderList):
    encoded = []
    for folder in folderList:
        encode = []
        for image in folder:
            img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            en = face_recognition.face_encodings(img)[0]
            encode.append(en)
        encoded.append(encode)
    return encoded

print("Started..")
encodeListKnown = findEncodings(studentsImageList)
encodeListKnownWithFolders = [encodeListKnown,studentImageFolders]
print("Completed!")

file = open("EncodedFile.p","wb")
pickle.dump(encodeListKnownWithFolders,file)
file.close()
print("File saved!")






