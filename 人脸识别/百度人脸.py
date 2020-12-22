from aip import AipFace
import base64
import cv2 as cv
import numpy as np
import threading
    
def baidu_init():
    APP_ID = '14645910'
    API_KEY = 'ytLF4jOVsTSGP7BdcWGsfDb6'
    SECRET_KEY = 'K9TMBAWbWwHASZ0mQnw1UBTKXWVTMM1R'
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    return client

def draw_div(path,r):
    img=cv.imread(path)
    cv.namedWindow("Image",cv.WINDOW_NORMAL)
    num=r['result']['face_num']
    for i in range(num):
        height=int(r['result']['face_list'][i]['location']['height'])
        left=int(r['result']['face_list'][i]['location']['left'])
        top=int(r['result']['face_list'][i]['location']['top'])
        width=int(r['result']['face_list'][i]['location']['width'])
        cv.rectangle(img,(left,top),(left+width,top+height),(0,255,0),3)
    return img
client=baidu_init()

image = base64.b64encode(open('1.jpg', 'rb').read())
imageType = "BASE64"
image=str(image,'utf-8')
options={}
options["max_face_num"] = 10
r=client.detect(image,imageType,options)

img=draw_div('1.jpg',r)
cv.imshow("Image",img)
cv.waitKey(0)
cv.destroyAllWindows()
