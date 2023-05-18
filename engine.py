import numpy as np
import face_recognition
import cv2
import os
from datetime import datetime
import time
import dlib
import mysql.connector

class FaceRecognitionSystem():
    def __init__(self):
        self.last_recognition = None
        self.is_logging_enabled = True
        self.start_time = datetime.now()
        self.write_to_log = True
        self.encodeListKnown = []
        self.namesListKnown = []

    def connect_to_db(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qw123",
            database="diploma"
        )
        return mydb

    def find_encodings_from_db(self):
        encodeList = []
        namesList = []
        mydb = self.connect_to_db()

        cursor = mydb.cursor()
        cursor.execute("SELECT first_name, last_name, patronymic, face_photo FROM people")
        rows = cursor.fetchall()

        for row in rows:
            first_name, last_name, patronymic, photo = row
            img = cv2.imdecode(np.asarray(bytearray(photo), dtype=np.uint8), cv2.IMREAD_COLOR)

            if img is not None:  # Check for empty image
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                try:
                    encode = face_recognition.face_encodings(img)[0]
                    encodeList.append(encode)
                    name = f"{first_name} {last_name} {patronymic}"
                    namesList.append(name)
                    print(f"Found face on photo: {name}")
                except IndexError:
                    print(f"Error: No face found on photo: {name}")
            else:
                print(f"Empty image for: {first_name} {last_name} {patronymic}")

        mydb.close()
        self.encodeListKnown = encodeList
        self.namesListKnown = namesList

    def mark_attendance(self, name, current_time):
        mydb = self.connect_to_db()
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

    def start_recognition(self):
        self.find_encodings_from_db()
        print("Decoding completed")

        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = self.namesListKnown[matchIndex]

                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    current_time = datetime.now()
                    time_diff = current_time - self.last_recognition if self.last_recognition is not None else self.start_time
                    if self.is_logging_enabled and (datetime.now() - self.start_time).total_seconds() >= 5:
                        self.start_time = datetime.now()
                        self.write_to_log = True
                    else:
                        self.write_to_log = False

                    if self.write_to_log:
                        self.mark_attendance(name, current_time)

            cv2.imshow("Camera", img)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q') or k == 27:
                break

        cv2.destroyAllWindows()
        cap.release()
        cv2.waitKey(1)
