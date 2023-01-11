from mixed_class import mixed_class
import cv2
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
img = cv2.imread("C:\\Users\\farza\\Desktop\\Mass-Test_P_00066_LEFT_MLO.tiff")
m = mixed_class(img)
m.predict()