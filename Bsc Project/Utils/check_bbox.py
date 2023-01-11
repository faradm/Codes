import csv
import cv2
import pydicom
from process_low_res import get_img_from_folder
import skimage.color
import numpy as np
x = None

file_d = open('./mass_case_description_test_set.csv', 'r')
d_cdv = csv.DictReader(file_d)
d_csv = []
for xx in d_cdv:
    d_csv.append(xx)

with open('./retina_test_annotations.csv') as file:
    x = csv.DictReader(file)

    if x is not None:
        for i, case_ in enumerate(x):
            file_name = case_['img_path'].replace("/content/retina", "./retina")
            names = file_name.split('/')
            name = names[-1]
            name = name.split('.')
            name = name[0]
            if "Test" in file_name:
                case_img = cv2.imread(file_name)
                [mask_imgs, fullmammo_img, fullmammo_dcm_file, x_rois] = get_img_from_folder(name)
                for j in range(len(mask_imgs)):
                    mask_imgs[j] = cv2.resize(mask_imgs[j], (case_img.shape[1], case_img.shape[0]), interpolation=cv2.INTER_AREA)
                    print(mask_imgs[j].shape)
                    print(case_img.shape)
                    # mask_imgs[j] = skimage.color.gray2rgb(mask_imgs[j])
                    case_img[mask_imgs[j].astype(np.bool) == 1] = [100, 0, 100]
                    box = [case_['x1'], case_['y1'], case_['x2'], case_['y2']]
                    b = np.array(box).astype(int)
                    cv2.rectangle(case_img, (b[0], b[1]), (b[2], b[3]), [100, 0, 0], lineType=cv2.LINE_AA)
                cv2.imshow('s', case_img)
                cv2.waitKey(0)
            else:
                pass