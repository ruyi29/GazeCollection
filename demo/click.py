import cv2
import numpy as np

n = 20                  # 手动设置照片编号
subject = 'Chen'        # 填入你的编号
width = 1300            # 指定窗口宽度
height = 720            # 指定窗口高度
RADIUS_MAX = 25         # 圆点最大半径

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
# （事件（鼠标移动、左键、右键），横坐标，纵坐标，组合键，setMouseCallback的userdata用于传参）
def mouse_callback(event, x, y, flags, userdata):
    if event == cv2.EVENT_LBUTTONDOWN:    # 拍摄照片
        global n, X, Y, radius, count
        error = 10
        if n % 21 == 0 or n % 22 == 0:
            error = 1000000
            cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
            X , Y = -1, -1
        if (x-X) ** 2 + (y-Y) ** 2 < error:  # 点击位置与实际位置误差较小时
            # ret, frame = cap.read()
            SaveData()

            cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
            X = np.random.randint(0, width)
            Y = np.random.randint(0, height)
            radius = RADIUS_MAX
            count = 0
            n += 1
            cv2.circle(img, (X, Y), radius, (0, 0, 0), -1)

            cv2.imshow('Screen', img)  # 显示图像


if __name__ == '__main__':
    # 初始化窗口
    print("Let's start!")
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Screen')  # 创建窗口
    cv2.setMouseCallback('Screen', mouse_callback)  # 将回调函数绑定到窗口

    img = np.ones((height, width, 3), dtype=np.uint8) * 255  # 创建白色的图像
    X = np.random.randint(0, width)  # 生成随机坐标
    Y = np.random.randint(0, height)
    radius = RADIUS_MAX  # 圆点半径
    cv2.circle(img, (X, Y), radius, (0, 0, 0), -1)
    cv2.imshow('Screen', img)  # 显示图像
    count = 0

    while True:
        ret, frame = cap.read()
        # cv2.imshow("Capture", frame)

        # 圆点变化
        count = count + 1
        if radius > 5:   # 圆点变小
            if count == 2:
                radius = radius - 1
                cv2.circle(img, (X, Y), RADIUS_MAX, (255, 255, 255), -1)
                cv2.circle(img, (X, Y), radius, (0, 0, 0), -1)
                cv2.imshow('Screen', img)
                count = 0
        elif count > 10000:   # 停留时间过长圆点会更新
            cv2.circle(img, (X, Y), 10, (255, 255, 255), -1)
            X = np.random.randint(0, width)
            Y = np.random.randint(0, height)
            radius = RADIUS_MAX
            cv2.circle(img, (X, Y), radius, (0, 0, 0), -1)
            cv2.imshow('Screen', img)
            count = 0

        k = cv2.waitKey(1) & 0xFF
        if k == ord(' '):  # 按’空格‘退出
            break
        # elif cv2.getWindowProperty('Capture', 0) == -1:  # 使窗口可以正常关闭
        #     break

    cap.release()
    cv2.destroyAllWindows()