import cv2
import numpy as np
import os


n = 20                  # 手动设置照片编号
subject = 'Chen'        # 填入你的编号
width = 1300            # 指定窗口宽度
height = 720            # 指定窗口高度
RADIUS_MAX = 25         # 圆点最大半径
    

# 创建文件夹
def CreateFile():
    if not os.path.exists('data'):
        os.makedirs('data', exist_ok=True)

    if not os.path.exists('data/coordinate.txt'):
        with open('data/coordinate.txt', 'w') as f:
            pass
    
    if not os.path.exists('data/Photo'):
        os.makedirs('data/Photo', exist_ok=True)


# 初始化圆点和数据
def InitDraw():
    global n, X, Y, radius, speed, F, disappear, event_begin
    F = -1
    speed = 0
    disappear = 0
    event_begin = 1  # 保证连续两次鼠标出发事件不会出错
    X = np.random.randint(5, width - 40)  # 生成随机坐标
    Y = np.random.randint(5, height - 20)
    radius = RADIUS_MAX  # 圆点半径
    cv2.rectangle(img, (0, 0), (200, 100), (255, 255, 255), -1)
    cv2.circle(img, (X, Y), radius, (0, 0, 255), -1)
    cv2.circle(img, (X, Y), 5, (0, 0, 0), -1)
    ShowInfo()
    cv2.imshow('Screen', img)  # 显示图像

# 信息展示
def ShowInfo():
    global n
    cv2.putText(img, str(n), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    if n % 2 == 0:
        cv2.putText(img, "Upright", (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    else:
        cv2.putText(img, "NotUpright", (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)


# 保存数据
def SaveData():
    global n, X, Y
    cv2.imwrite("./data/Photo/" + str(n) + '.jpg', frame)
    print("save " + str(n) + ".jpg", end = ' ')     # 提示拍摄成功用的
    data = str(n) + ',' + subject + ',' + str(n) + '.jpg,' + str(X) + ',' + str(Y) + '\n'
    with open('data/coordinate.txt', 'a') as f:
        f.write(data)
    print(f'({X}, {Y})')
    n += 1


# 回调函数：鼠标点击输出点击的坐标
#（事件（鼠标移动、左键、右键），横坐标，纵坐标，组合键，setMouseCallback的userdata用于传参）
def mouse_callback(event, x, y, flags, userdata):
    global event_begin, disappear
    if event == cv2.EVENT_LBUTTONDOWN and event_begin == 1:    # 拍摄照片
        global n, X, Y, radius, speed, F
        event_begin = 0
        cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)

        if n % 21 == 0 or n % 22 == 0:
            cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
            X , Y = -1, -1
            SaveData()
        else:
            # 画布中生成数字
            num = np.random.randint(1, 5)
            cv2.putText(img, str(num), (X - 5, Y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.imshow('Screen', img)
            cv2.waitKey(300)
            cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
            ShowInfo()
            cv2.imshow('Screen', img)
            
            # 如果选择了正确的选项
            key = cv2.waitKey(0) & 0xFF
            if key == ord(str(num)):  # 按’空格‘退出
                SaveData()

        InitDraw()


if __name__ == '__main__':
    print("Let's start!")
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Screen')  # 创建窗口
    cv2.setMouseCallback('Screen', mouse_callback)  # 将回调函数绑定到窗口
    img = np.ones((height, width, 3), dtype = np.uint8) * 255  # 创建白色的图像
    CreateFile()
    InitDraw()
    
    while True:
        ret, frame = cap.read()
        # cv2.imshow("Capture", frame)

        # 圆点变化 
        speed = speed + 1
        disappear = disappear + 1
        if radius > 5:   # 圆点变小
            if speed == 1:
                radius = radius + F
                cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
                cv2.circle(img, (X, Y), radius, (0, 0, 255), -1)
                cv2.circle(img, (X, Y), 5, (0, 0, 0), -1)
                ShowInfo()
                cv2.imshow('Screen', img)
                speed = 0
                if radius == 5 or radius == RADIUS_MAX:   # 圆点变小
                    F = F * -1
                    radius = radius + F

        # 停留时间过长圆点会更新
        if disappear > 10000:   
            cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
            InitDraw()

        # 按’空格‘退出
        k = cv2.waitKey(1) & 0xFF
        if k == ord(' '):  
            break

    cap.release()
    cv2.destroyAllWindows()