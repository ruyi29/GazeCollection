import cv2
import numpy as np
import os

num = 0  # 每次手动设置

# 回调函数：鼠标点击输出点击的坐标
# （事件（鼠标移动、左键、右键），横坐标，纵坐标，组合键，setMouseCallback的userdata用于传参）
def mouse_callback(event, x, y, flags, userdata):
    if event == cv2.EVENT_LBUTTONDOWN:    # 拍摄照片
        global num
        num += 1
        print(str(x)+','+str(y))


# 初始化窗口
width = 500  # 指定窗口大小
height = 1000
cap = cv2.VideoCapture(0)
cv2.namedWindow('Screen')  # 创建窗口
cv2.setMouseCallback('Screen', mouse_callback)  # 将回调函数绑定到窗口
img = np.ones((height, width, 3), dtype=np.uint8) * 255  # 创建白色的图像
cv2.imshow('Screen', img)  # 显示图像
cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()



