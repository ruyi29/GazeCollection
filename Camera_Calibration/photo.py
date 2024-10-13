import cv2
import numpy as np
import os

num = 50  # 每次手动设置
if not os.path.exists('./Camera_Calibration/images'):
    os.makedirs('./Camera_Calibration/images', exist_ok=True)

# 回调函数：鼠标点击输出点击的坐标
# （事件（鼠标移动、左键、右键），横坐标，纵坐标，组合键，setMouseCallback的userdata用于传参）
def mouse_callback(event, x, y, flags, userdata):
    if event == cv2.EVENT_LBUTTONDOWN:    # 拍摄照片
        global num
        num += 1
        cv2.imwrite("./images/" + str(num) + '.jpg', frame)
        print("save" + str(num) + ".jpg successfuly!")            # 提示拍摄成功用的

# 初始化窗口
width = 400  # 指定窗口大小
height = 200
cap = cv2.VideoCapture(0)
cv2.namedWindow('Screen')  # 创建窗口
cv2.setMouseCallback('Screen', mouse_callback)  # 将回调函数绑定到窗口
img = np.ones((height, width, 3), dtype=np.uint8) * 255  # 创建白色的图像
cv2.imshow('Screen', img)  # 显示图像
count = 0

while True:
    ret, frame = cap.read()
    cv2.imshow("Capture", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):  # 按q退出
        break
    elif cv2.getWindowProperty('Capture', 0) == -1:  # 使窗口可以正常关闭
        break

cap.release()
cv2.destroyAllWindows()



