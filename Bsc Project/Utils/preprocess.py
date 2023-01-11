import cv2
import os
import numpy as np
import scipy.misc

DIR = 'D:\Education\Electrical Engineering\Assignments\Final Project\PData'
TRAIN = os.path.join(DIR, 'train')
VALID = os.path.join(DIR, 'val')
COMPLETE = 'D:\Education\Electrical Engineering\Assignments\Final Project\Dataset\ROI\\roi\Tif'

for x in [TRAIN, VALID]:
    for y in ["Mass", 'Normal']:
        imgs_paths = os.listdir(os.path.join(x, y))
        ii = 0
        for file in imgs_paths:
            if(os.path.isdir(os.path.join(x, y, file))):
                continue
            # os.rename(os.path.join(x, y, file), os.path.join(x, y, f"{ii}.tif"))
            # ii = ii + 1
            X = cv2.imread(os.path.join(x, y, file))
            X_average = np.mean(X)
            X = X - X_average
            contrast = np.sqrt(0 + np.mean(X**2))
            X = 1 * X / max(contrast, 1e-8)
            # scipy can handle it
            scipy.misc.imsave(os.path.join(x, y, file), X)