import numpy as np
import face_recognition
import cv2
import os
from datetime import datetime
import time
import dlib
import mysql.connector

def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="qw123",
        database="diploma"
    )
    return mydb

def findEncodingsFromDB():
    encodeList = []
    namesList = []
    mydb = connect_to_db()

    cursor = mydb.cursor()
    cursor.execute("SELECT first_name, last_name, patronymic, face_photo FROM people")
    rows = cursor.fetchall()

    for row in rows:
        first_name, last_name, patronymic, photo = row
        img = cv2.imdecode(np.asarray(bytearray(photo), dtype=np.uint8), cv2.IMREAD_COLOR)

        if img is not None:  # Проверка на пустое изображение
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
                name = f"{first_name} {last_name} {patronymic}"
                namesList.append(name)
                print(f"Найдено лицо на фото {name}")
            except IndexError:
                print(f"Ошибка: на фото {name} не найдено лицо")
        else:
            print(f"Пустое изображение для {first_name} {last_name} {patronymic}")

    mydb.close()
    return encodeList, namesList

status_dict = {}

last_recognition = None


def markAttendance(name, current_time):
    mydb = connect_to_db()
    cursor = mydb.cursor()
    cursor.execute("SELECT COUNT(*) FROM recognition_log WHERE first_name = %s AND last_name = %s AND patronymic = %s AND time_exit IS NULL", name.split())
    result = cursor.fetchone()
    count = result[0]
    if count == 0:
        sql = "INSERT INTO recognition_log (first_name, last_name, patronymic, time_entry) VALUES (%s, %s, %s, %s)"
        val = name.split() + [current_time]
    else:
        sql = "UPDATE recognition_log SET time_exit = %s, time_spent = TIMEDIFF(time_exit, time_entry) WHERE first_name = %s AND last_name = %s AND patronymic = %s AND time_exit IS NULL"
        val = [current_time] + name.split()
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()



cap = cv2.VideoCapture(0)

is_logging_enabled = True
start_time = datetime.now()
write_to_log = True

cap = cv2.VideoCapture(0)

is_logging_enabled = True
start_time = datetime.now()
write_to_log = True

encodeListKnown, namesListKnown = findEncodingsFromDB()
print("Декодирование закончено")

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = namesListKnown[matchIndex]

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            current_time = datetime.now()
            time_diff = current_time - last_recognition if last_recognition is not None else start_time
            if is_logging_enabled and (
                    datetime.now() - start_time).total_seconds() >= 5:  # Раз в 5 секунд будут записываться данные в БД
                start_time = datetime.now()
                write_to_log = True
            else:
                write_to_log = False

            if write_to_log:
                markAttendance(name, current_time)

    cv2.imshow("Camera", img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') or k == 27:
        break

cv2.destroyAllWindows()
cap.release()
cv2.waitKey(1)