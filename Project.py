from abc import ABC, abstractmethod
from tkinter import *
import cv2
import numpy as np


class Tennis_ball_detect(ABC):
    @abstractmethod
    def main(self, img): pass
    x, y, w, h =0,0,0,0

class GeneralControl(Tennis_ball_detect):

    def main(self, img):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        myColors = [[40, 50, 30, 142, 255, 255]] #Enter values here

        for color in myColors:
            lower = np.array(color[0:3])
            upper = np.array(color[3:6])
            mask = cv2.inRange(imgHSV, lower, upper)
            result = cv2.bitwise_and(img,img,mask=mask)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 500:
                    cv2.drawContours(img, cnt, -1, (0, 255, 0), 3)

                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                    self.x,self.y,self.w,self.h = cv2.boundingRect(approx)
                    strXY=str(int(self.x)) + "," + str(int(self.y))

                    cv2.putText(img,strXY,(self.x+self.y//2,self.y+self.w//2),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0))
            cv2.imshow("mask", mask)
            cv2.imshow("result", result)



frameWidth = 426
frameHeight = 240
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 130)
window = Tk()
window.geometry("600x600")
window.title("Tennis Ball Project")

label1 = Label(window, text='Tennis Ball Project', relief="solid", width=20, font=("arial", 19, "bold"))
label1.place(x=90, y=55)

label2 = Label(window, text='Name,Surname = Gürkan Sönmez', width=30, font=("arial", 15, "bold"))
label2.place(x=90, y=130)

label3 = Label(window, text='****************', width=30, font=("arial", 15, "bold"))
label3.place(x=90, y=180)

label4 = Label(window, text='  Please close the window to continue.', width=40, font=("arial", 8, "bold"))
label4.place(x=90, y=250)

label5 = Label(window, text='Press the "q" button to exit while the program is running.', width=50,
               font=("arial", 8, "bold"))
label5.place(x=90, y=300)

window.mainloop()

while True:

    _, img = cap.read()
    project = GeneralControl()
    project.main(img)
    window.mainloop()
    cv2.imshow("Tennis Ball Project", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
