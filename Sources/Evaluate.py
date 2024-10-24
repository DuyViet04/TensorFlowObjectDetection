from Detector import DetectImage
import os
import cv2
folder_path = 'D:\TestPictureDataAI'

# Duyệt qua tất cả các tệp trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg'):
        image_path = os.path.join(folder_path,  filename)
        TestImage = cv2.imread(image_path)
        cv2.imshow('DetectedImg', DetectImage(TestImage,0.4))
        cv2.waitKey(0)