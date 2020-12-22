#导入cv模块
import cv2 as cv

#导入Matplotlib
from matplotlib import pyplot as plt

#读取图像，支持 bmp、jpg、png、tiff 等常用格式
img = cv.imread("1.jpg")
#画出一个方块
cv.rectangle(img,(384,0),(510,128),(0,255,0),3)
#创建窗口(可省略)并显示图像
cv.namedWindow("Image",cv.WINDOW_NORMAL)
cv.imshow("Image",img)

cv.waitKey(0)#等待某键摁下

plt.imshow(img,cmap='gray',interpolation='bicubic')
plt.xticks([]),plt.yticks([])#隐藏X和Y轴上的刻度值
plt.show()

#释放窗口
cv.destroyAllWindows()
