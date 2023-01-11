import os
import random

DIR = 'D:\\Education\\Electrical Engineering\\Assignments\\Final Project\\PData'
TRAIN = os.path.join(DIR, 'train')
VALID = os.path.join(DIR, 'val')
MASS = "Mass"
NORMAL = "Normal"
COMPLETE = 'D:\\Education\\Electrical Engineering\\Assignments\\Final Project\\Dataset\\ROI\\roi\\Tif'

train_files_m = os.listdir(os.path.join(TRAIN, MASS))
train_files_n = os.listdir(os.path.join(TRAIN, NORMAL))
random.shuffle(train_files_m)
random.shuffle(train_files_n)

NUMBER_OF_VAL = 350

for i in range(350):
    os.rename(os.path.join(TRAIN, MASS, train_files_m[i]), os.path.join(VALID, MASS, train_files_m[i]))
    os.rename(os.path.join(TRAIN, NORMAL, train_files_n[i]), os.path.join(VALID, NORMAL, train_files_n[i]))