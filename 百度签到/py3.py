import numpy as np
import base64
import cv2 as cv
#opencv3
from aip import AipFace
import threading
import time

def baidu_init():
    '''
    百度ai初始化
    '''
    APP_ID = '14645910'
    API_KEY = 'ytLF4jOVsTSGP7BdcWGsfDb6'
    SECRET_KEY = 'K9TMBAWbWwHASZ0mQnw1UBTKXWVTMM1R'
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    return client


def trans_bin(img):
    '''
    cv2格式转base64
    '''
    img_encode = cv.imencode('.jpg', img)[1]
    base64_data = str(base64.b64encode(img_encode))[2:-1]
    #data_encode = np.array(img_encode)
    return base64_data

def find_position(real_1):
    '''
    找人脸坐标
    client:初始化信息 j:人脸坐标信息
    '''
    global j
    global client
    imageType = "BASE64"
    image=trans_bin(real_1)
    #image=str(image,'utf-8')
    options={}
    options["max_face_num"] = 10
    """ 可选参数 """
    j=client.detect(image,imageType,options)

def face_search(face_token):
    '''
    人脸查找
    '''
    groupIdList = "1"   #人脸库名
    """ 如果有可选参数 """
    options = {}
    #options["quality_control"] = "NORMAL"
    #options["liveness_control"] = "LOW"
    #options["user_id"] = "233451"
    #options["max_user_num"] = 3
    r=client.search(face_token,'FACE_TOKEN', groupIdList, options)
    return r

def draw_div():
    '''
    画人脸框
    '''
    global j
    global frame
    global j1
    if(j['error_msg']!='SUCCESS'):
        #print(j)
        j=j1
    j1=j
    num=j['result']['face_num']
    
    for i in range(num):
        height=int(j['result']['face_list'][i]['location']['height'])
        left=int(j['result']['face_list'][i]['location']['left'])
        top=int(j['result']['face_list'][i]['location']['top'])
        width=int(j['result']['face_list'][i]['location']['width'])
        cv.rectangle(real,(left,top),(left+width,top+height),(255,0,0),3) 

def thread1():
    '''
    线程1：画框并显示
    '''
    global frame
    global real
    while(1):
        ret,real=cap.read()
        frame=real
        try:
            draw_div()
        except:
            pass
        cv.imshow('test',frame)
        if cv.waitKey(1)&0xFF == ord('q'):
            break
def thread2():
    '''
    线程2：找人脸坐标
    '''
    time.sleep(3)
    while(1):
        find_position(real)

def thread3():
    '''
    线程3：人脸查找
    (list)l 记录签到过的id
    '''
    global l
    time.sleep(5)
    while(1):
        j_3=j
        if(j_3['error_msg']!='SUCCESS'):
            continue
        num=j_3['result']['face_num']
        for i in range(num):
            face_token=j_3['result']['face_list'][i]["face_token"]
            r=face_search(face_token)
            if(r['error_msg']=='SUCCESS'):
                if((r['result']['user_list'][0]['group_id'],r['result']['user_list'][0]['user_id']) in l):
                    continue
                print('-------------------成功--------------------')
                print(r['result']['user_list'][0]['group_id'],r['result']['user_list'][0]['user_id'])
                l.append((r['result']['user_list'][0]['group_id'],r['result']['user_list'][0]['user_id']))
        
if __name__ == "__main__":
    l=list()
    client=baidu_init()
    lock=threading.Lock()
    cap=cv.VideoCapture(0) # 0 为摄像头
    t1 = threading.Thread(target=thread1)
    t1.setDaemon(True)
    t1.start()
    t2=threading.Thread(target=thread2)
    t2.start()
    t3=threading.Thread(target=thread3)
    t3.start()

    
