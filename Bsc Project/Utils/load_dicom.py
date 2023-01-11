import pydicom
import numpy as np
import cv2
from matplotlib import pyplot as plt


x = pydicom.dcmread('./000000.dcm')
y = x.pixel_array
cv2.imwrite('full.tiff', y)