import cv2
import numpy as np
import os
import glob
import xml.etree.ElementTree as ET

# 填写编号
cam_id = 1
file_name = 'cam' + str(cam_id).zfill(2) + '.xml'
root = './Camera_Calibration/'
new_file_path = root + file_name

# 修改写入的矩阵格式
def Trans(data):
    # 将矩阵元素转换为字符串，并用科学记数法格式化
    new_data = []
    for row in data:
        for value in row:
            # 转换为科学记数法
            scientific_value = f"{value:.15e}"
            new_data.append(scientific_value)
    return ' '.join(new_data)

# 创建xml文件
def CreateXML(mtx, dist):
    # 读取XML文件
    global root, new_file_path
    file_path = root + 'cam00.xml'  # 替换为你的XML文件路径
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 修改Camera_Matrix中的data元素
    new_camera_matrix_data = Trans(mtx)
    camera_matrix = root.find('Camera_Matrix/data')
    if camera_matrix is not None:
        camera_matrix.text = new_camera_matrix_data
        # print("Camera_Matrix中的data已修改。")

    # 修改Distortion_Coefficients中的data元素
    new_distortion_coefficients_data = Trans(dist)
    distortion_coefficients = root.find('Distortion_Coefficients/data')
    if distortion_coefficients is not None:
        distortion_coefficients.text = new_distortion_coefficients_data
        # print("Distortion_Coefficients中的data已修改。")

    # 保存修改后的XML到新的文件
    tree.write(new_file_path, xml_declaration=True)
    # print(f"修改后的数据已保存到新文件: {new_file_path}")
    print(f"相机内参文件已生成: {new_file_path}")


# 定义棋盘格的尺寸
CHECKERBOARD = (6, 9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 创建向量以存储每个棋盘图像的 3D 点向量
objpoints = []
# 创建向量以存储每个棋盘图像的 2D 点向量
imgpoints = []

# 定义 3D 点的世界坐标
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp = objp * 200
prev_img_shape = None

# 提取存储在给定目录中的单个图像的路径
images = glob.glob(root + 'images/*.jpg')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 找到棋盘角
    # 如果在图像中找到所需数量的角，则 ret = true
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    """
    如果检测到所需数量的角， 我们细化像素坐标并可视化
    """
    if ret == True:
        objpoints.append(objp)
        # 细化给定二维点的像素坐标。
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        imgpoints.append(corners2)

        # 绘制并显示角
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)

    cv2.imshow('img', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()

h, w = img.shape[:2]

"""
通过传递已知 3D 点 (objpoints) 的值 和检测到的角点（imgpoints）对应的像素坐标 实现相机标定
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# print("Camera matrix : \n")
# print(mtx)
# print("dist : \n")
# print(dist)
# print("rvecs : \n")
# print(rvecs)
# print("tvecs : \n")
# print(tvecs)

# 创建标定数据文件
CreateXML(mtx, dist)