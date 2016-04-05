import cv
import time
import math
import sys
import numpy as np
import cv2
import time


class Target:
    nVuelta = 175921
    grado = 175921 / 360
    modo = 0
    v = 0
    p = 0
    p_actual = 0
    unidad_base_p = 0.1
    unidad_base_v = 1
    ingresando_unidad = False
    input_unidad = ""
    tecla = 0

    er = (0, 0, 0)
    w = 0
    aux1 = 0

    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        cv.NamedWindow("Target", 1)
        cv.NamedWindow("Threshold1", 2)
        cv.NamedWindow("Threshold2", 2)
        # cv.NamedWindow("hsv",2)

    def run(self):
        start = time.time()
        d = 0
        # initiate fontcalc
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
        # instantiate images
        hsv_img = cv.CreateImage(cv.GetSize(cv.QueryFrame(self.capture)), 8, 3)
        threshold_img1 = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        threshold_img1a = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        threshold_img2 = cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
        i = 0

        while True:
            # print ser.readline()
            # capture the image from the cam
            img = cv.QueryFrame(self.capture)

            # convert the image to HSV
            cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)

            # threshold the image to isolate two colors
            cv.InRangeS(hsv_img, (165, 155, 110), (250, 200, 150), threshold_img1)  # red
            cv.InRangeS(hsv_img, (0, 155, 110), (10, 200, 150), threshold_img1a)  # red again
            cv.InRangeS(hsv_img, (160, 100, 100), (179, 255, 255), threshold_img1)  # otro red
            cv.Add(threshold_img1, threshold_img1a, threshold_img1)  # this is combining the two limits for red
            cv.InRangeS(hsv_img, (85, 175, 130), (130, 255, 255), threshold_img2)  # blue
            cv.InRangeS(hsv_img, (100, 135, 135), (140, 255, 255), threshold_img2)  # otro blue

            # determine the moments of the two objects
            threshold_img1 = cv.GetMat(threshold_img1)
            threshold_img2 = cv.GetMat(threshold_img2)
            moments1 = cv.Moments(threshold_img1, 0)
            moments2 = cv.Moments(threshold_img2, 0)
            area1 = cv.GetCentralMoment(moments1, 0, 0)
            area2 = cv.GetCentralMoment(moments2, 0, 0)

            # initialize x and y
            x1, y1, x2, y2, x3, y3 = (1, 2, 3, 4, 5, 6)
            coord_list = [x1, y1, x2, y2]
            for x in coord_list:
                x = 0

            # there can be noise in the video so ignore objects with small areas
            if (area1 > 20000):
                # x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                x1 = int(cv.GetSpatialMoment(moments1, 1, 0) / area1)
                y1 = int(cv.GetSpatialMoment(moments1, 0, 1) / area1)

                # draw circle
                cv.Circle(img, (x1, y1), 2, (0, 255, 0), 20)

                # write x and y position
                # cv.PutText(img,str(x1)+","+str(y1),(x1,y1+20),font, 255) #Draw the text

            if (area2 > 20000):
                # x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                x2 = int(cv.GetSpatialMoment(moments2, 1, 0) / area2)
                y2 = int(cv.GetSpatialMoment(moments2, 0, 1) / area2)

                # draw circle
                cv.Circle(img, (x2, y2), 2, (0, 255, 0), 20)

                # cv.PutText(img,str(x2)+","+str(y2),(x2,y2+20),font, 255) #Draw the text
                cv.Line(img, (x1, y1), (x2, y2), (0, 255, 0), 4, cv.CV_AA)
                # draw line and angle
                cv.Line(img, (x1, y1), (cv.GetSize(img)[0], y1), (100, 100, 100, 100), 4, cv.CV_AA)
            x3 = x2
            y3 = y2
            x1 = float(x1)
            y1 = float(y1)
            x2 = float(x2)
            y2 = float(y2)
            if (x2 == x1):
                angle = 90
            else:
                angle = math.atan((y1 - y2) / (x2 - x1)) * 180 / math.pi
            end = time.time()
            t = end - start
            d = d + (math.sqrt(math.pow((x3 - x1), 2) + math.pow((y3 - y1), 2))) / 1000
            cv.PutText(img, "{0:.2f}".format(angle) + "," + "{0:.2f}".format(t) + "," + "{0:.2f}".format(d),
                       (int(x1) + 50, (int(y2) + int(y1)) / 2), font, 255)

            Kp = 40
            Ki = 0.001
            Kd = 0.1

            e = -angle
            # print(e)
            dT = end - self.aux1

            self.aux1 = end
            dw = self.PID(Kp, Ki, Kd, e, dT)
            self.w = self.w + dw
            # print dw
            # time.sleep(0.1)
            # print self.w

            print self.w

            ser2.write("EN\r\n".encode())
            aux = "v" + str(int(self.w)) + "\r\n"
            ser2.write(aux.encode())
            # cv.WriteFrame(writer,img)


            # display frames to users
            # cv.PutText(img,"hola",(int(x1)+50,(int(y2)+int(y1))/2),font,255)
            cv.ShowImage("Target", img)
            # cv.ShowImage("Threshold1",threshold_img1)
            # cv.ShowImage("Threshold2",threshold_img2)
            # cv.ShowImage("hsv",hsv_img)
            # c = cv2.waitKey(1)
            if self.GUI() == 1:  # DESCOMENTAR ESTA WEA
                break

        cv.DestroyAllWindows()

    # el codigo es una linea asi que pico con hacer un metodo
    # def WriteSerial(self):
    #    ser.write

    def PID(self, Pp, Pi, Pd, e, dT):

        self.er = (e, self.er[0], self.er[1])

        dw = Pp * (self.er[2] - self.er[1]) + Pi * self.er[2] * dT + Pd * (
        self.er[2] - 2 * self.er[1] + self.er[0]) / dT

        return dw

if __name__ == "__main__":
    t = Target()
    t.run()
