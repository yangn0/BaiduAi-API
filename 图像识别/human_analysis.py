from aip import AipBodyAnalysis
import json
import cv2 as cv

APP_ID ='11589803'
API_KEY ='K2WOMV1pCyI1IXIbvawDDRhu'
SECRET_KEY = 'VxQRvsETnYHsEZsWi9lGrLhhV5Q1slaX'
client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)

#读取照片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
#绘制方块
def print_div(a,j):
    img=cv.imread(a)
    for i in range(j['person_num']):
        cv.rectangle(img,(int(j['person_info'][i]['location']['left']),int(j['person_info'][i]['location']['top'])),
                 (int(j['person_info'][i]['location']['left']+j['person_info'][i]['location']['width']),int(j['person_info'][i]['location']['top']+j['person_info'][i]['location']['height'])),
                 (0,255,0),3)
    cv.namedWindow("Image",cv.WINDOW_NORMAL)
    cv.imshow("Image",img)
    cv.waitKey(0)
    cv.destroyAllWindows()
#选择功能
def select_power():
    i=input('''

                     选择需要的功能

                    1.人体关键点识别
                    2.人体属性识别
                    3.人流量统计
    ''')
    return int(i)
if __name__ == "__main__":    
    while(1):
        a=input('请输入图片(小于4M)的位置：')
        image = get_file_content(a)

        i=select_power()
        if(i==1):
            """ 调用人体关键点识别 """
            j=client.bodyAnalysis(image)
            """decode（’utf-8’）表示将utf-8编码的字符串转换成unicode编码。
            encode(‘gb2312’)，表示将unicode编码的字符串转换成gb2312编码。"""
            print(json.dumps(j,sort_keys=True,indent=4,separators=(',',':')))
            print_div(a,j)

        if(i==2):
            """ 调用人体属性识别
            client.bodyAttr(image);"""
            """ 如果有可选参数 """
            options = {}
            options["type"] = "gender,age"
            """ 带参数调用人体属性识别 """
            j=client.bodyAttr(image, options)
            d=json.dumps(j,sort_keys=True,indent=4,separators=(',',':'),ensure_ascii=False)
            print(d)

        if(i==3):
            """ 调用人流量统计 
            client.bodyNum(image);"""
            """ 如果有可选参数 """
            options = {}
            options["area"] = "" #x1,y1,x2,y2,x3,y3...xn,yn
            options["show"] = "false"

            """ 带参数调用人流量统计 """
            j=client.bodyNum(image)
            print(json.dumps(j,sort_keys=True,indent=4,separators=(',',':'),ensure_ascii=False))



