import os
import tensorflow as tf
import cv2
import numpy as np

# 0 is negative, 1 is benign calcification, 2 is benign mass, 3 is malignant calcification, 4 is malignant mass
NEGATIVE = 0
BEN_CAL = 1
BEN_MASS = 2
MAL_CAL = 3
MAL_MASS = 4

ROOT = 'D:\Education\Electrical Engineering\Assignments\Final Project\Dataset\ddsm-mammography'
TF_RECORD_DIR = os.path.join(ROOT, 'training')

NEGATIVE_DIR = os.path.join(TF_RECORD_DIR, "negative")
BEN_CAL_DIR = os.path.join(TF_RECORD_DIR, "benign_calcification")
BEN_MASS_DIR = os.path.join(TF_RECORD_DIR, "benign_mass")
MAL_CAL_DIR = os.path.join(TF_RECORD_DIR, "malignant_calcification")
MAL_MASS_DIR = os.path.join(TF_RECORD_DIR, "malignant_mass")


def decode(serial_data):

    features = tf.io.parse_single_example(
            serial_data,
            features={
                'label': tf.FixedLenFeature([], tf.int64),
                'label_normal': tf.FixedLenFeature([], tf.int64),
                'image': tf.FixedLenFeature([], tf.string)
            })

    # extract the data
    label_normal = features['label_normal']
    image = tf.decode_raw(features['image'], tf.uint8)
    label = features['label']
    # reshape and scale the image
    image = tf.reshape(image, [299, 299, 1])

    return image, label, label_normal

def save_train():
    files = os.listdir(TF_RECORD_DIR)

    data_sets = []
    sess = tf.compat.v1.Session()
    for file in files:
        if os.path.isdir(os.path.join(TF_RECORD_DIR, file)) == True:
            continue
        tf_file_path = os.path.join(TF_RECORD_DIR, file)
        dataset = tf.data.TFRecordDataset(tf_file_path)
        im_data = dataset.map(decode)
        data_sets.append(im_data)
    

    i = 0
    for dataset in data_sets:
        it = dataset.make_one_shot_iterator()
        next_element = it.get_next()
        print('here!')
        try:
            while True:
                img, label, label_normal = sess.run(next_element)
                label = int(label)
                save_dir = ''
                if label == 0:
                    save_dir = NEGATIVE_DIR
                elif label == 1:
                    save_dir = BEN_CAL_DIR
                elif label == 2:
                    save_dir = BEN_MASS_DIR
                elif label == 3:
                    save_dir = MAL_CAL_DIR
                elif label == 4:
                    save_dir = MAL_MASS_DIR
                else:
                    print('Else!!!')
                # print(label)
                # print(save_dir)
                # print(os.path.join(save_dir, str(i)+".png"))
                # cv2.imshow("s", img)
                # cv2.waitKey(0)
                cv2.imwrite(os.path.join(save_dir, str(i)+".png"), img)
                i = i + 1
        except tf.errors.OutOfRangeError:
            pass
        # for val in dataset:
        #     c = sess.run(val)
        #     print(c)
if __name__ == "__main__":
    save_train()
    # data = np.load('D:\Education\Electrical Engineering\Assignments\Final Project\Dataset\ddsm-mammography\cv10_data\cv10_data.npy')
    # data2 = np.load('D:\Education\Electrical Engineering\Assignments\Final Project\Dataset\ddsm-mammography\\test10_data\\test10_data.npy')
    # print(data.shape)
    # print(data2.shape)