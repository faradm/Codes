'''
retina_class is used to ease making prediction using RetinaNet library. The class inherits QRunnable so MainWindow.py can execute this 
class in a seperate thread and UI freezing is prevented. this class provides run method which performs prediction on a single image and emits result as a signal.
'''






from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time
from PySide2.QtCore import QRunnable, Slot
from yolov3_worker_signals import yolov3_worker_signals
import gc

# import keras
import keras
# import keras_retinanet
from keras_retinanet import models

# import miscellaneous modules

# set tf backend to allow memory to grow, instead of claiming everything
import tensorflow as tf
from keras_retinanet.preprocessing.csv_generator import CSVGenerator

class retina_class(QRunnable):
    
    def __init__(self, img):
        QRunnable.__init__(self)

        self.session = tf.Session()
        self.graph = tf.get_default_graph()
        with self.graph.as_default():
            with self.session.as_default():
                print("Retinanet Init")
        
        self.signals = yolov3_worker_signals()
        if img is not None:
            self.img = img  
        
        self.labels_to_names = {0: 'mass'}
        #ClassLable Info
        self.Class_Path = './keras-retinanet/data/class_mapping.csv'
        self.result_path = './keras-retinanet/logs'
        self.confidence_threshold = 0.25


    def set_img(self, img_):
        self.img = img_

    @Slot(np.ndarray)
    def run(self):
        
        ########
        model_path = os.path.join('./trained_models/resnet50_csv_best.h5')
        # load retinanet model
        with self.graph.as_default():
            with self.session.as_default():
                self.model = models.load_model(model_path, backbone_name='resnet50')
                self.model = models.convert_model(self.model)
                result, bboxes = self.predict(self.img)
                self.signals.img.emit(np.copy(result))
                self.signals.bboxes.emit(np.copy(bboxes))
        # Free memory
        del self.model
        del result
        # from numba import cuda
        # cuda.select_device(0)
        # cuda.close()
        gc.collect()

    def predict(self, Load_image):
        draw = Load_image.copy()
        draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
        image = Load_image
        image = preprocess_image(image)
        image, scale = resize_image(image)

        boxes, scores, labels = self.model.predict_on_batch(np.expand_dims(image, axis=0))
        
        boxes /= scale
        # visualize detections
        pred_bbox = np.array(boxes[0])
        pred_score = scores[0]
        pred_class_id = np.array(labels[0])
        row_num = 0
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            # scores are sorted so we can break
            if score < self.confidence_threshold:
                pred_bbox = np.delete(pred_bbox, row_num, axis=0)
                pred_score = np.delete(pred_score, row_num, axis=0)
                pred_class_id = np.delete(pred_class_id, row_num)
                continue
            color = label_color(label)
            b = box.astype(int)
            draw_box(draw, b, color=color)

            row_num = row_num + 1
        
        return draw, pred_bbox

    def get_session(self, tf):
        # config = tf.ConfigProto()
        # config.gpu_options.allow_growth = True
        config = tf.ConfigProto(device_count = {'CPU' : 1,'GPU' : 0})
        return tf.Session(config=config)

    def trim_zeros(self, x):
        """It's common to have tensors larger than the available data and
        pad with zeros. This function removes rows that are all zeros.

        x: [rows, columns].
        """

        assert len(x.shape) == 2
        return x[~np.all(x == 0, axis=1)]

    def compute_iou(self, box, boxes, box_area, boxes_area):
        """Calculates IoU of the given box with the array of the given boxes.
        box: 1D vector [y1, x1, y2, x2]
        boxes: [boxes_count, (y1, x1, y2, x2)]
        box_area: float. the area of 'box'
        boxes_area: array of length boxes_count.

        Note: the areas are passed in rather than calculated here for
        efficiency. Calculate once in the caller to avoid duplicate work.
        """
        # Calculate intersection areas
        y1 = np.maximum(box[0], boxes[:, 0])
        y2 = np.minimum(box[2], boxes[:, 2])
        x1 = np.maximum(box[1], boxes[:, 1])
        x2 = np.minimum(box[3], boxes[:, 3])
        intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
        union = box_area + boxes_area[:] - intersection[:]
        iou = intersection / union
        return iou

    def compute_overlaps(self, boxes1, boxes2):
        """Computes IoU overlaps between two sets of boxes.
        boxes1, boxes2: [N, (y1, x1, y2, x2)].

        For better performance, pass the largest set first and the smaller second.
        """
        # Areas of anchors and GT boxes
        area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
        area2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])

        # Compute overlaps to generate matrix [boxes1 count, boxes2 count]
        # Each cell contains the IoU value.
        overlaps = np.zeros((boxes1.shape[0], boxes2.shape[0]))
        for i in range(overlaps.shape[1]):
            box2 = boxes2[i]
            overlaps[:, i] = self.compute_iou(box2, boxes1, area2[i], area1)
        return overlaps


    def compute_matches(self, gt_boxes, gt_class_ids, pred_boxes, pred_class_ids, pred_scores, iou_threshold=0.5, score_threshold=0.0):
        """Finds matches between prediction and ground truth instances.

        Returns:
            gt_match: 1-D array. For each GT box it has the index of the matched
                    predicted box.
            pred_match: 1-D array. For each predicted box, it has the index of
                        the matched ground truth box.
            overlaps: [pred_boxes, gt_boxes] IoU overlaps.
        """
        # Trim zero padding
        # TODO: cleaner to do zero unpadding upstream
        gt_boxes = self.trim_zeros(gt_boxes)
        # gt_masks = gt_masks[..., :gt_boxes.shape[0]]
        pred_boxes = self.trim_zeros(pred_boxes)
        pred_scores = pred_scores[:pred_boxes.shape[0]]
        # Sort predictions by score from high to low
        indices = np.argsort(pred_scores)[::-1]
        pred_boxes = pred_boxes[indices]
        pred_class_ids = pred_class_ids[indices]
        pred_scores = pred_scores[indices]
        # pred_masks = pred_masks[..., indices]

        # Compute IoU overlaps [pred_masks, gt_masks]
        overlaps = self.compute_overlaps(pred_boxes, gt_boxes)

        # Loop through predictions and find matching ground truth boxes
        match_count = 0
        pred_match = -1 * np.ones([pred_boxes.shape[0]])
        gt_match = -1 * np.ones([gt_boxes.shape[0]])
        for i in range(len(pred_boxes)):
            # Find best matching ground truth box
            # 1. Sort matches by score
            sorted_ixs = np.argsort(overlaps[i])[::-1]
            # 2. Remove low scores
            low_score_idx = np.where(overlaps[i, sorted_ixs] < score_threshold)[0]
            if low_score_idx.size > 0:
                sorted_ixs = sorted_ixs[:low_score_idx[0]]
            # 3. Find the match
            for j in sorted_ixs:
                # If ground truth box is already matched, go to next one
                if gt_match[j] > -1:
                    continue
                # If we reach IoU smaller than the threshold, end the loop
                iou = overlaps[i, j]
                if iou < iou_threshold:
                    break
                # Do we have a match?
                if pred_class_ids[i] == gt_class_ids[j]:
                    match_count += 1
                    gt_match[j] = i
                    pred_match[i] = j
                    break

        return gt_match, pred_match, overlaps

    def compute_stats(self, gt_boxes, gt_class_ids, pred_boxes, pred_class_ids, pred_scores, iou_threshold=0.5, score_threshold=0.0):

        gt_match, pred_match, overlaps = self.compute_matches(gt_boxes, gt_class_ids, pred_boxes, pred_class_ids, pred_scores, iou_threshold, score_threshold=score_threshold)

        TP = np.sum(pred_match > -1)
        FP = len(pred_match) - TP
        FN = len(gt_class_ids) - TP
        return TP, FP, FN


    