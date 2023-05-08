import cv2
class Add_Photo:
    def __init__(self, filename):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Не удалось получить доступ к камере")
            exit()
        else:
	        ret, frame = self.cap.read()
	        cv2.imwrite(filename, frame)
	        self.cap.release()