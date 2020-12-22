import numpy as np
import cv2 as cv
import human_analysis
from human_analysis import client
import threading
import time

#矩阵转二进制
def trans_bin(img):
    img_encode = cv.imencode('.jpg', img)[1]
    data_encode = np.array(img_encode)
    return data_encode.tostring()

'''def real_video(cap):
    global frame
    global real
    while(True):
        ret,real=cap.read() #第一个参数ret 为True 或者False,代表有没有读取到图片第二个参数frame表示截取到一帧的图片              
        cv.imshow('test',real)
        if cv.waitKey(1)&0XFF ==ord('q'):
            break'''
    
def find_position(real_1):
    global j
    j=client.bodyAnalysis(trans_bin(real_1))  

def draw_div():
    global j
    global frame
    for i in range(j['person_num']):
        cv.rectangle(frame,(int(j['person_info'][i]['location']['left']),int(j['person_info'][i]['location']['top'])),
                 (int(j['person_info'][i]['location']['left']+j['person_info'][i]['location']['width']),int(j['person_info'][i]['location']['top']+j['person_info'][i]['location']['height'])),
                 (0,255,0),3)   

def thread1():
    global frame
    global real
    while(1):
        ret,real=cap.read()
        frame=real
        draw_div()
        cv.imshow('test',frame)
        if cv.waitKey(1)&0xFF == ord('q'):
            break
def thread2():
    time.sleep(1)
    while(1):
        find_position(real)
        
j={'person_num': 1, 'person_info': [{'body_parts': {'neck': {'y': 391.2644958496094, 'x': 343.4131774902344}, 'left_shoulder': {'y': 389.9898376464844, 'x': 440.9325256347656}, 'left_knee': {'y': 0.0, 'x': 0.0}, 'left_ankle': {'y': 0.0, 'x': 0.0}, 'right_elbow': {'y': 0.0, 'x': 0.0}, 'nose': {'y': 277.8685607910156, 'x': 349.9180908203125}, 'left_hip': {'y': 0.0, 'x': 0.0}, 'right_hip': {'y': 0.0, 'x': 0.0}, 'left_wrist': {'y': 0.0, 'x': 0.0}, 'left_elbow': {'y': 0.0, 'x': 0.0}, 'right_shoulder': {'y': 391.3052062988281, 'x': 245.8436431884766}, 'right_ankle': {'y': 0.0, 'x': 0.0}, 'right_knee': {'y': 0.0, 'x': 0.0}, 'right_wrist': {'y': 0.0, 'x': 0.0}}, 'location': {'width': 0, 'top': 0, 'height': 0, 'left': 0}}], 'log_id': 8161337942681287969}       
if __name__ == "__main__":
    lock=threading.Lock()
    cap=cv.VideoCapture(0) # 0 为摄像头
    t1 = threading.Thread(target=thread1)
    t1.setDaemon(True)
    t1.start()
    t2=threading.Thread(target=thread2)
    t2.start()

    
