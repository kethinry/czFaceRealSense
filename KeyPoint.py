from mtcnn import MTCNN
import cv2
import os

path = "./faceverse"
dirs= os.listdir(path)
dirpath = "./KeyPointResult"
if not os.path.exists(dirpath):
    os.makedirs(dirpath)

for dir in dirs:
    files = os.listdir(path+"/"+dir)
    cnt = 0
    for file in files:
        keypoint = []
        img = cv2.cvtColor(cv2.imread(path+"/"+dir+"/"+file), cv2.COLOR_BGR2RGB)
        detector = MTCNN()
        x = detector.detect_faces(img)
        keypoint.append(list(x[0]['keypoints']['left_eye']))
        keypoint.append(list(x[0]['keypoints']['right_eye']))
        keypoint.append(list(x[0]['keypoints']['nose']))
        keypoint.append(list(x[0]['keypoints']['mouth_left']))
        keypoint.append(list(x[0]['keypoints']['mouth_right']))
        if not os.path.exists("./KeyPointResult/"+dir):
            os.makedirs("./KeyPointResult/"+dir)
        with open("./KeyPointResult/"+dir+"/"+str(cnt)+".txt", "w") as f:  # 设置文件对象
            for i in keypoint:  # 对于双层列表中的数据
                i = str(i).strip('[').strip(']').replace(',', '').replace('\'', '') + '\n'  # 将其中每一个列表规范化成字符串
                f.write(i)
            # img = cv2.cvtColor(cv2.imread("ivan.jpg"), cv2.COLOR_BGR2RGB)
        cnt = cnt+1
# img = cv2.cvtColor(cv2.imread("ivan.jpg"), cv2.COLOR_BGR2RGB)
#
# detector = MTCNN()
# x = detector.detect_faces(img)
# print(x)
# print(type(x))
# print(x[0]['keypoints']['nose'][0])