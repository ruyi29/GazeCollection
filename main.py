import cv2
import numpy as np
import os
import sys


light_condition = 7     # 手动设置光照情况编号
subject = 'Chen_glass'  # 填入你的编号
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

    if not os.path.exists('data/Video'):
        os.makedirs('data/Video', exist_ok=True)


# 按 enter 键继续, 空格键退出
def PressEnter():
    cv2.putText(img, 'Press Enter to Continue', 
                (width // 4, height // 3 * 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
    cv2.imshow('Screen', img)
    while True:
        k = cv2.waitKey(0) & 0xFF
        if k == 13:
            break
        if k == ord(' '):  
            sys.exit()


# 初始化圆点和数据
def InitDraw():
    global n, X, Y, radius, speed, F, disappear, event_begin
    F = -1
    speed = 0
    disappear = 0
    event_begin = 1  # 保证连续两次鼠标出发事件不会出错
    X = np.random.randint(5, width - 40) 
    Y = np.random.randint(5, height - 20)
    radius = RADIUS_MAX  # 圆点半径
    cv2.rectangle(img, (0, 0), (width, height), (255, 255, 255), -1)
    if n % 22 == 21 or n % 22 == 0:
        cv2.putText(img, 'Please look out of the screen and click', (width // 8, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4)
    else:
        cv2.circle(img, (X, Y), radius, (0, 0, 255), -1)
        cv2.circle(img, (X, Y), 5, (0, 0, 0), -1)
    cv2.putText(img, str(n), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.imshow('Screen', img) 


# 保存数据
def SaveData():
    global n, X, Y, count
    cv2.imwrite("./data/Photo/" + str(n) + '.jpg', frame)
    print("save " + str(n) + ".jpg", end = ' ')     # 提示拍摄成功用的
    data = str(n) + ',' + subject + ','  + str(light_condition) + ',' + str(count) + ',' + str(n) + '.jpg,' + str(X) + ',' + str(Y) + ',' + '\n'
    with open('data/coordinate.txt', 'a') as f:
        f.write(data)
    print(f'({X}, {Y})')

    # 结束时
    if n == light_condition * 12 * 22:
        cv2.rectangle(img, (0, 0), (width, height), (255, 255, 255), -1)
        cv2.putText(img, 'Finish', (width // 2 - 50, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4)
        cv2.imshow('Screen', img)
        PressEnter()
        sys.exit()

    # 具体情况提示
    if n % 22 == 0:
        cv2.rectangle(img, (0, 0), (width, height), (255, 255, 255), -1)
        Guide()
        PressEnter()
        
    n += 1

    


# 流程引导
def Guide():
    global n
    case_num = n // 22 + 1   # 具体情况编号
    # 坐姿端正
    text = 'Sit_Upright' if case_num % 2 == 1 else 'Not_Upright'
    cv2.putText(img, text, (width // 10, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    
    # 设备距离
    text = 'Distance(70cm+)'
    t = (case_num - 1) // 4 % 3
    if t == 1:
        text = 'Distance(45-48cm)'
    elif t == 2:
        text = 'Distance(32-35cm)'
    cv2.putText(img, text, (width // 3, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    
    # 设备倾角
    text = 'Angle(30)'
    t = (case_num - 1) // 2 % 2
    if t == 1:
        text = 'Angle(15)'
    cv2.putText(img, text, (width // 4 * 3, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)

    cv2.imshow('Screen', img)
    

# 回调函数：鼠标点击输出点击的坐标
#（事件（鼠标移动、左键、右键），横坐标，纵坐标，组合键，setMouseCallback的userdata用于传参）
def mouse_callback(event, x, y, flags, userdata):
    global event_begin, disappear
    if event == cv2.EVENT_LBUTTONDOWN and event_begin == 1:    # 拍摄照片
        global n, X, Y, radius, speed, F
        event_begin = 0
        cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)

        if n % 22 == 21 or n % 22 == 0:
            cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
            X , Y = -1, -1
            SaveData()
        else:
            # 画布中生成随机数
            num = np.random.randint(1, 5)
            cv2.putText(img, str(num), (X - 5, Y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.imshow('Screen', img)
            cv2.waitKey(300)
            cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
            cv2.putText(img, str(n), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.imshow('Screen', img)
            
            # 如果选择了正确的选项
            k = cv2.waitKey(0) & 0xFF
            if k == ord(str(num)):  # 按’空格‘退出
                SaveData()
            elif k == ord(' '):  
                sys.exit()
            else:
                cv2.putText(img, 'Wrong Choose', (width // 2 - 150, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4)
                cv2.imshow('Screen', img)
                cv2.waitKey(1500)  # 等待（）毫秒

        InitDraw()


if __name__ == '__main__':

    # 相机
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter('./data/Video/' + str(light_condition) + '.avi', fourcc, 30.0, (640, 480))
    cap = cv2.VideoCapture(0)

    # 窗口
    cv2.namedWindow('Screen')  # 创建窗口
    cv2.setMouseCallback('Screen', mouse_callback)  # 将回调函数绑定到窗口
    img = np.ones((height, width, 3), dtype = np.uint8) * 255  # 创建白色的图像

    # 文件夹
    CreateFile()
    
    # 提示当前光照情况
    LIGHT_CONDITION = ['Daytime_Inside_FrontLight', 'Daytime_Inside_SideLight', 'Daytime_Inside_BackLight', 
                       'Daytime_Outside_AndLight', 'Night_Inside_TopLight', 'Night_Inside_ScreenLight', 
                       'Night_TableLamp_FrontLight', 'Night_TableLamp_SideLight', 'Night_Inside_OutsideLight']
    print(LIGHT_CONDITION[light_condition - 1] + ' Start')
    cv2.putText(img, LIGHT_CONDITION[light_condition - 1] + ' Start', 
                (width // 4, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
    cv2.imshow('Screen', img)
    PressEnter()
    
    n = (light_condition - 1) * 22 * 12 + 1  # 第 n 张照片
    cv2.rectangle(img, (0, 0), (width, height), (255, 255, 255), -1)
    Guide()
    PressEnter()

    # 初始化
    count = 0   # 记录当前是第几帧
    InitDraw()
    
    while True:
        count += 1
        ret, frame = cap.read()
        video.write(frame)
        cv2.imshow("Capture", frame)

        if not(n % 22 == 21) and not(n % 22 == 0):
            # 圆点变化 
            speed = speed + 1
            disappear = disappear + 1
            if radius > 5:   # 圆点变小
                if speed == 1:
                    radius = radius + F
                    cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
                    cv2.circle(img, (X, Y), radius, (0, 0, 255), -1)
                    cv2.circle(img, (X, Y), 5, (0, 0, 0), -1)
                    cv2.putText(img, str(n), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                    cv2.imshow('Screen', img)
                    speed = 0
                    if radius == 5 or radius == RADIUS_MAX:   # 圆点变小
                        F = F * -1
                        radius = radius + F

            # 停留时间过长圆点更新
            if disappear > 1000:   
                cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
                InitDraw()

        # 按'空格'退出
        k = cv2.waitKey(1) & 0xFF
        if k == ord(' '):  
            break

    cap.release()
    video.release()
    cv2.destroyAllWindows()