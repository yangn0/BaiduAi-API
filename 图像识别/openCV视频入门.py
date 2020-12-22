import numpy as np
import cv2 as cv

cap=cv.VideoCapture(0)


while(1):
    ret,real=cap.read()
    #frame=real
    cv.imshow('test',real)
    if cv.waitKey(1)&0xFF == ord('q'):
        break
#释放捕获
cap.release()
cv.destroyAllWindows()
    
