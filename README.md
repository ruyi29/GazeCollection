# 用户手册

## 程序简介

该程序用于采集人眼在屏幕上的注视点信息

### 主程序 - main.py
1. 运行程序后，屏幕中出现一个被红圈包围的黑点，注视黑点并在任意位置点击鼠标后，圆点消失，原位置短暂出现数字1-4，在键盘上选择正确的数字才能出发数据保存，按下其他键则continue。
2. 当照片编号为21或22的正数倍时，应看向电脑屏幕外并点击鼠标。（具体操作按照程序提示操作即可）

## 操作流程

### 环境配置

打开IDE，在终端中运行脚本`bash run.sh`

### 运行代码

请依据`Condition.md`中的表格调整好环境后，运行`main.py`

### 后期检查

打开data文件夹中的照片进行查看，若发现存在‘面部不完整’或者‘眼睛部分有遮挡’的情况，请删除该照片和coordinate.txt中对应编号的数据，并重新采集
