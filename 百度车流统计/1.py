from aip import AipImageClassify
import requests
import json
import base64
import cv2 as cv
import threading
from multiprocessing import Process
import multiprocessing
import time
import numpy as np

def get_access_token():
    """ 你的 APPID AK SK """
    APP_ID = '11221151'
    API_KEY = 'E6rpi9H1ZYbFRabkDGsXX5pQ'
    SECRET_KEY = 'WLjluXvAdFvWwB1WSrgpN9VGknIxnvMf'
    #client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    access_token_url = 'https://aip.baidubce.com/oauth/2.0/token'
    r = requests.post(access_token_url, data={
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY,
    })
    d = json.loads(r.text)
    return d['access_token']


def trans_bin(img):
    '''
    cv2格式转base64
    '''
    img_encode = cv.imencode('.jpg', img)[1]
    base64_data = str(base64.b64encode(img_encode))[2:-1]
    #data_encode = np.array(img_encode)
    return base64_data


def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString,np.uint8)  
    image = cv.imdecode(nparr,cv.IMREAD_COLOR)
    return image

def worker1(public_l):
    '''
    展示图片
    '''
    cap = cv.VideoCapture('jiankong.mp4')
    while(1):
        ret, real = cap.read()
        public_l['data1']=real
        #cv.rectangle(real,(public_l['left'],public_l['top']),(public_l['left']+public_l['width'],public_l['top']+public_l['height']),(255,0,0),3) 
        if(public_l['data2']==''):
            continue
        cv.imshow('test', base64_cv2(public_l['data2']))
        if cv.waitKey(150) & 0xFF == ord('q'):
            break

def worker2(public_l):
    '''
    处理图片
    '''
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    access_token = get_access_token()
    traffic_flow_url='https://aip.baidubce.com/rest/2.0/image-classify/v1/traffic_flow?access_token='+access_token
    case_id=int(time.time())
    while(1):
        data={
            'case_id':case_id,
            'case_init':'false',
            'image':trans_bin(public_l['data1']),
            'show':'true',
            'area':'177,14,601,14,601,157,177,157'
        }
        r=requests.post(traffic_flow_url,headers=headers,data=data)
        d=json.loads(r.text)
        #print(d)
        try:
            public_l['data2']=d['image']
        except:
            continue

if __name__ =="__main__":
    
    public_l=multiprocessing.Manager().dict()   #主进程与子进程共享这个字典
    public_l['data1']=''
    public_l['data2']=''
    public_l['left']=10
    public_l['top']=10
    public_l['width']=10
    public_l['height']=10

    p1 = Process(target=worker1, args=(public_l,))
    p1.start()

    p2=Process(target=worker2, args=(public_l,))
    p2.start()

    p1.join()
    print('Child process end.')