import os
import numpy as np
import cv2
import pydicom
import pandas as pd
from rm_back import check_if_rect_in_back
import time
import random

DEBUG_HELP = False

PATCH_WIDTH = 224
PATCH_LENGTH = 224
CENTER_WINDOW = 1
MASS_OUT_PERCENT = 0.03
NORMAL_OUT_PERCENT = 0.95
HORIZONTAL_MOVE = 4
VERTICAL_MOVE = 4

def get_path(root, app):
    return root + app


root_dir = 'D:\\Education\\Electrical Engineering\\Assignments\\Final Project\\'
roi_dir = 'Dataset\\ROI\\roi\\CBIS-DDSM'
fullmammo_dir = 'Dataset\\FullMammo\\CBIS-DDSM'
# benign_dir = 'Dataset\\Benign'
# malignant_dir = 'Dataset\\Malignant'
mass_patch_save_dir = 'Dataset\\Patch\\Mass'
normal_patch_save_dir = 'Dataset\\Patch\\Normal'
csv_file_dir = 'Dataset'
FILE_NAME0 = '000001.dcm'
FILE_NAME1 = '000000.dcm'
CSV_FILE_NAME = 'mass_case_description_train_set.csv'
fullmammo_folders = os.listdir(get_path(root_dir, fullmammo_dir))
roi_folders = os.listdir(get_path(root_dir, roi_dir))
inner_dir = ''

csv_file = pd.read_csv(os.path.join(get_path(root_dir, csv_file_dir), CSV_FILE_NAME))

def conv_roi_inner_dir_to_fullmammo_inner_dir(roi_inner):
    splitted = roi_inner.split("_")
    splitted.pop()
    f = ''
    for i in range(len(splitted)):
        if(i!=len(splitted) - 1):
            f = f + splitted[i] + '_'
        else:
            f = f + splitted[i]
    return f


def is_in_forg(xi, yi, mask_img, backg_img, out_percent):
    xi_h = min(xi+PATCH_WIDTH, mask_img.shape[1])
    yi_h = min(yi+PATCH_LENGTH, mask_img.shape[0])
    if(xi_h <= xi or yi_h <= yi):
        pass
    t = backg_img[yi:yi_h,xi:xi_h]
    tt = np.sum(np.sum(t))

    if(tt <= (1 - out_percent) * (xi_h - xi) * (yi_h - yi)):
        return True
    else:
        return False

def contains_mass(row, col, mask_img, backg_img):
    temp = mask_img[max(0, col+PATCH_LENGTH//2-CENTER_WINDOW):min(col+PATCH_LENGTH//2+CENTER_WINDOW, mask_img.shape[0]), max(0, row+PATCH_WIDTH//2-CENTER_WINDOW):min(row+PATCH_WIDTH//2+CENTER_WINDOW, mask_img.shape[1])]
    temp = np.sum(np.sum(temp))
    if(temp > 0):
        return True
    else:
        return False

def check_if_mirror(backg_mask):
    [y_l, x_l] = backg_mask.shape
    sum_l = np.sum(backg_mask[:, 0:x_l//3])
    sum_r = np.sum(backg_mask[:, 2*x_l//3:])
    return sum_r <= sum_l 

def debug_draw_rect(xi, yi, fullmammo_img):
    if(DEBUG_HELP):
        test_copy = np.copy(fullmammo_img)
        cv2.rectangle(test_copy, (xi, yi), (xi+PATCH_WIDTH, yi+PATCH_LENGTH), 65535, 20)
        test_copy = cv2.resize(test_copy, (600, 600*test_copy.shape[0]//test_copy.shape[1]))
        cv2.imshow('Scan rect!', test_copy)
        cv2.waitKey(0)

def debug_draw_found_patch(xi, yi, fullmammo_img):
    if(DEBUG_HELP):
        test_copy = np.copy(fullmammo_img)
        cv2.rectangle(test_copy, (xi, yi), (xi+PATCH_WIDTH, yi+PATCH_LENGTH), 65535, 20)
        test_copy = cv2.resize(test_copy, (600, 600*test_copy.shape[0]//test_copy.shape[1]))
        cv2.imshow('Patch found!', test_copy)
        cv2.waitKey(0)

def get_img_from_folder(x, num_of_images):
    print(x)
    x_fullmammo = conv_roi_inner_dir_to_fullmammo_inner_dir(x)
    if(os.path.isdir(os.path.join(get_path(root_dir, roi_dir), x)) == False):
        roi_folders.remove(x)
        return None
    else:
        num_of_images = num_of_images + 1
        inner_dir = os.path.join(get_path(root_dir, roi_dir), x)
        fullmammo_inner_dir = os.path.join(get_path(root_dir, fullmammo_dir), x_fullmammo)
        # inner_dir = os.path.join(inner_dir, os.listdir(inner_dir)[0])
        # inner_dir = os.path.join(inner_dir, os.listdir(inner_dir)[0])
        fullmammo_inner_dir = os.path.join(fullmammo_inner_dir, os.listdir(fullmammo_inner_dir)[0])
        fullmammo_inner_dir = os.path.join(fullmammo_inner_dir, os.listdir(fullmammo_inner_dir)[0])
        # if os.path.getsize(os.path.join(inner_dir, FILE_NAME0)) > os.path.getsize(os.path.join(inner_dir, FILE_NAME1)):
        #     mask_dcm_file = pydicom.dcmread(os.path.join(inner_dir, FILE_NAME0))
        # else:
        #     mask_dcm_file = pydicom.dcmread(os.path.join(inner_dir, FILE_NAME1))
        if(len(os.listdir(inner_dir))==1):
            inner_dir = os.path.join(inner_dir, os.listdir(inner_dir)[0])
            inner_dir = os.path.join(inner_dir, os.listdir(inner_dir)[0])
            if(len(os.listdir(inner_dir)) < 2):
                return None
            if os.path.getsize(os.path.join(inner_dir, FILE_NAME0)) > os.path.getsize(os.path.join(inner_dir, FILE_NAME1)):
                mask_dcm_file = pydicom.dcmread(os.path.join(inner_dir, FILE_NAME0))
            else:
                mask_dcm_file = pydicom.dcmread(os.path.join(inner_dir, FILE_NAME1))
        elif(len(os.listdir(inner_dir))==2):
            inner_dir0 = os.path.join(inner_dir, os.listdir(inner_dir)[0])
            inner_dir0 = os.path.join(inner_dir0, os.listdir(inner_dir0)[0])
            inner_dir1 = os.path.join(inner_dir, os.listdir(inner_dir)[1])
            inner_dir1 = os.path.join(inner_dir1, os.listdir(inner_dir1)[0])
            if os.path.getsize(os.path.join(inner_dir0, FILE_NAME1)) > os.path.getsize(os.path.join(inner_dir1, FILE_NAME1)):
                mask_dcm_file = pydicom.dcmread(os.path.join(inner_dir0, FILE_NAME1))
            else:
                mask_dcm_file = pydicom.dcmread(os.path.join(inner_dir1, FILE_NAME1))
        
        fullmammo_dcm_file = pydicom.dcmread(os.path.join(fullmammo_inner_dir, FILE_NAME1))
        if(fullmammo_dcm_file is None):
            return None
        mask_img = mask_dcm_file.pixel_array
        fullmammo_img = fullmammo_dcm_file.pixel_array
        return mask_img, fullmammo_img, fullmammo_dcm_file, num_of_images

def extract_normal_patch(fullmammo_img, mask_img, normal_patch_per_img, one_more):
    backg_mask = check_if_rect_in_back(fullmammo_img, fullmammo_dcm_file.SmallestImagePixelValue, fullmammo_dcm_file.LargestImagePixelValue, False)
    mirror = check_if_mirror(backg_mask)
    if(mirror):
        mask_img = cv2.flip(mask_img, 1)
        fullmammo_img = cv2.flip(fullmammo_img, 1)
        backg_mask = cv2.flip(backg_mask, 1)
    for i in range(normal_patch_per_img + one_more):
        while(True):
            yi = np.random.randint(fullmammo_img.shape[0]//4, 3*fullmammo_img.shape[0]//4)
            xi = np.random.randint(fullmammo_img.shape[1]//4, 3*fullmammo_img.shape[1]//4)
            if(is_in_forg(xi, yi, mask_img, backg_mask, NORMAL_OUT_PERCENT) and not(contains_mass(xi, yi, mask_img, backg_mask))):
                break
        patch = fullmammo_img[yi:yi+PATCH_LENGTH, xi:xi+PATCH_WIDTH]
        debug_draw_found_patch(xi, yi, fullmammo_img)
        cv2.imwrite(os.path.join(root_dir, normal_patch_save_dir,  x + str(i) + ".tiff"), patch)


def extract_mass_patch(fullmammo_img, mask_img, num_of_mass_patch):
    more_patch_exist = True
    xi = 0; yi = 0
    patch_idx_in_img = 0
    backg_mask = check_if_rect_in_back(fullmammo_img, fullmammo_dcm_file.SmallestImagePixelValue, fullmammo_dcm_file.LargestImagePixelValue, False)
    mirror = check_if_mirror(backg_mask) #TODO: Check if algorithm works for every image
    if(mirror):
        mask_img = cv2.flip(mask_img, 1)
        fullmammo_img = cv2.flip(fullmammo_img, 1)
        backg_mask = cv2.flip(backg_mask, 1)
    while(more_patch_exist):
        if(yi >= fullmammo_img.shape[0] - PATCH_LENGTH):
            more_patch_exist = False
            break
        if(xi >= fullmammo_img.shape[1] - PATCH_WIDTH or not(is_in_forg(xi, yi, mask_img, backg_mask, MASS_OUT_PERCENT))):
                yi = yi + PATCH_LENGTH//VERTICAL_MOVE
                xi = 0
                if(yi >= fullmammo_img.shape[0] - PATCH_LENGTH):                     
                    more_patch_exist = False
                    break
        debug_draw_rect(xi, yi, fullmammo_img)
        if(contains_mass(xi, yi, mask_img, backg_mask)):
            patch = fullmammo_img[yi:yi+PATCH_LENGTH, xi:xi+PATCH_WIDTH]
            debug_draw_found_patch(xi, yi, fullmammo_img)
            cv2.imwrite(os.path.join(root_dir, mass_patch_save_dir,  x + str(patch_idx_in_img) + ".tiff"), patch)
            patch_idx_in_img = patch_idx_in_img + 1
            num_of_mass_patch = num_of_mass_patch + 1
        xi = xi + PATCH_WIDTH//HORIZONTAL_MOVE
    return num_of_mass_patch

if __name__ == "__main__":
    num_of_mass_patch = 0 
    num_of_images = 0
    errors_ = []
    ### Extracting mass patches
    for x in roi_folders:
        temp = None
        try:
            temp = get_img_from_folder(x, num_of_images)
        except:
            errors_.append(x)
            print("Error on file roi" + x)
            roi_folders.remove(x)
            continue
        if(temp is None):
            errors_.append(x)
            print("Error on file roi" + x)
            roi_folders.remove(x)
            continue
        else:
            [mask_img, fullmammo_img, fullmammo_dcm_file, temp_num_of_images] = temp 
            # Extract patches and increment number of mass
            temp2 = None
            try:
                temp2 = extract_mass_patch(fullmammo_img, mask_img, num_of_mass_patch)
            except:
                errors_.append(x)
                print("Error on file fullmammo" + x)
                roi_folders.remove(x)
                continue
            if(temp2 is not None):
                num_of_mass_patch = temp2
                num_of_images = temp_num_of_images
            else:
                errors_.append(x)
                print("Error on file fullmammo" + x)
                roi_folders.remove(x)
                continue
    print(num_of_mass_patch)
    print(num_of_images)
    print(errors_)