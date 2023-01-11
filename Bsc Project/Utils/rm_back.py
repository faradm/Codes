import pydicom
import numpy as np
import cv2
from matplotlib import pyplot as plt


def check_if_rect_in_back(x_, smallest_val, largest_val, flip = False):
    if(flip):
        x_ = cv2.flip(x_, 1)
    x_ = x_ - smallest_val
    x_ = np.round(x_/(largest_val-smallest_val)*255).astype(np.uint16)
    NUMBER_OF_BINS = 256
    hist = cv2.calcHist([x_],[0],None,[NUMBER_OF_BINS],[0,255])
    p = hist / np.sum(hist)
    temp = (np.arange(NUMBER_OF_BINS) + 1).reshape(-1, 1)
    w = np.cumsum(p)
    muKK = np.cumsum(p * temp)
    sigma2B = (muKK[-1]*w[1:-1] - muKK[1:-1])**2 / (w[1:-1]*(1-w[1:-1]))
    sigma2B = sigma2B[np.isfinite(sigma2B)]
    kstar = np.argmax(sigma2B)
    y = x_
    z = np.zeros(y.shape)
    z[y < kstar] = 1
    z[y >= kstar] = 0
    return z