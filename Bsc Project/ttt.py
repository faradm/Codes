import cv2


from retina_class import retina_class


retina = retina_class()
img = cv2.imread("C:\\Users\\farza\Desktop\\Mass-Test_P_00016_LEFT_CC.tiff")
retina.predict(img)