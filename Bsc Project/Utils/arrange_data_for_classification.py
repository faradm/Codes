import os
import numpy as np
import cv2
import pydicom
import pandas as pd

dir = 'D:\Education\Electrical Engineering\Assignments\Final Project\Dataset\ROI\\roi\CBIS-DDSM\\'
benign_dir = 'D:\Education\Electrical Engineering\Assignments\Final Project\Dataset\ROI\Benign\\'
malignant_dir = 'D:\Education\Electrical Engineering\Assignments\Final Project\Dataset\ROI\Malignant\\'
FILE_NAME0 = '000001.dcm'
FILE_NAME1 = '000000.dcm'
CSV_FILE_NAME = 'mass_case_description_train_set.csv'
img_folders = os.listdir(dir)
inner_dir = ''

csv_file = pd.read_csv(os.path.join(csv_file_dir, CSV_FILE_NAME))

for x in img_folders:
    #print(x)
    if(os.path.isdir(os.path.join(dir, x)) == False):
        img_folders.remove(x)
    else:
        inner_dir = os.path.join(dir, x)
        if(len(os.listdir(inner_dir))==1):
            inner_dir = os.path.join(inner_dir, os.listdir(inner_dir)[0])
            inner_dir = os.path.join(inner_dir, os.listdir(inner_dir)[0])
            if(len(os.listdir(inner_dir)) < 2):
                continue
            if os.path.getsize(os.path.join(inner_dir, FILE_NAME0)) < os.path.getsize(os.path.join(inner_dir, FILE_NAME1)):
                dcm_file = pydicom.dcmread(os.path.join(inner_dir, FILE_NAME0))
            else:
                dcm_file = pydicom.dcmread(os.path.join(inner_dir, FILE_NAME1))
        elif(len(os.listdir(inner_dir))==2):
            inner_dir0 = os.path.join(inner_dir, os.listdir(inner_dir)[0])
            inner_dir0 = os.path.join(inner_dir0, os.listdir(inner_dir0)[0])
            inner_dir1 = os.path.join(inner_dir, os.listdir(inner_dir)[1])
            inner_dir1 = os.path.join(inner_dir1, os.listdir(inner_dir1)[0])
            if os.path.getsize(os.path.join(inner_dir0, FILE_NAME1)) < os.path.getsize(os.path.join(inner_dir1, FILE_NAME1)):
                dcm_file = pydicom.dcmread(os.path.join(inner_dir0, FILE_NAME1))
            else:
                dcm_file = pydicom.dcmread(os.path.join(inner_dir1, FILE_NAME1))
        #print('test:')
        cancer_type = csv_file.loc[csv_file['ROI mask file path'].str.contains(x)]
        cancer_type = cancer_type['pathology']
        folder = ''
        if(cancer_type.iloc[0].upper().find('BENIGN') != -1):
            folder = benign_dir
        else:
            folder = malignant_dir
        dcm_img = dcm_file.pixel_array
        cv2.imwrite(folder + '/' + x + '.tif', dcm_img)