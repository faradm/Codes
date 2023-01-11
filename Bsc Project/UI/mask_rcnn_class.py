'''
mask_rcnn_class is used to ease making prediction using Mask MRCNN library. The class inherits QRunnable so MainWindow.py can execute this 
class in a seperate thread and UI freezing is prevented. this class provides run method which performs prediction on a single image and emits result as a signal.
'''




import os
import sys
import random
import math
import re
import time
import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
from imgaug import augmenters as iaa
import pickle as pkl
import skimage.color

# Root directory of the project
ROOT_DIR = os.path.abspath("")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library

from mrcnn.config import Config
import mrcnn.model as modellib
from mrcnn import visualize

from PySide2.QtCore import QRunnable, Slot
from yolov3_worker_signals import yolov3_worker_signals
import gc

class MassConfig(Config):
    """Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    
    BACKBONE = "resnet101"
    # Give the configuration a recognizable name
    NAME = "masses"

    # Train on 1 GPU and 8 images per GPU. We can put multiple images on each
    # GPU because the images are small. Batch size is 8 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 4#Old 4

    # Number of classes (including background)
    NUM_CLASSES = 2  # background + 3 shapes

    # Use small images for faster training. Set the limits of the small side
    # the large side, and that determines the image shape.
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512

    RPN_NMS_THRESHOLD = 0.9
    
    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE = 128

    # Use a small epoch since the data is simple
    STEPS_PER_EPOCH = (1240)//IMAGES_PER_GPU
    
    # use small validation steps since the epoch is small
    VALIDATION_STEPS = 200//IMAGES_PER_GPU#Old 50
    MEAN_PIXEL = [54.61, 54.61, 54.61]
    STD_MY = 1
    USE_MINI_MASK = True
    LEARNING_RATE = 0.001



class InferenceConfig(MassConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    DETECTION_MIN_CONFIDENCE = 0.90
    MEAN_PIXEL = [54.61, 54.61, 54.61]
    STD_MY = 1


class mask_rcnn_class(QRunnable):

    def __init__(self, img=None):
        QRunnable.__init__(self)
        self.session = modellib.tf.Session()
        self.graph = modellib.tf.get_default_graph()
        
        with self.graph.as_default():
            with self.session.as_default():
                print("Mask RCNN Init")
        if img is not None:
            self.img = img
        self.signals = yolov3_worker_signals()
        # Directory to save logs and trained model
        self.MODEL_DIR = os.path.join(ROOT_DIR, "logs")
        self.inference_config = InferenceConfig()
        self.class_names = ['BG', 'Mass']
        
    def set_img(self, img_):
        self.img = img_

    @Slot(np.ndarray)
    def run(self):
        with self.graph.as_default():
            with self.session.as_default():
                model = modellib.MaskRCNN(mode="inference", 
                                config=self.inference_config,
                                model_dir=self.MODEL_DIR)

                model_path = os.path.join('./mrcnn/weights', "mask_3+_coco_16_.h5")

                print("Loading weights from ", model_path)
                model.load_weights(model_path, by_name=True)

                results = model.detect([self.img], verbose=0)

                r = results[0]

                result = visualize.display_instances(self.img, r['rois'], r['masks'], r['class_ids'], 
                                                self.class_names, r['scores'])
                self.signals.img.emit(np.copy(result))
                self.signals.bboxes.emit(np.copy(r['rois']))
        del model
        del results
        # from numba import cuda
        # cuda.select_device(0)
        # cuda.close()
        gc.collect()
