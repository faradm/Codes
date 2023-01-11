from darknet.darknet_class import darknet_class
from mask_rcnn_class import mask_rcnn_class
from PySide2.QtCore import Qt, Slot, QThreadPool
from retina_class import retina_class

class mixed_class:

    def __init__(self, img=None):
        self.darknet = darknet_class(img)
        self.mask_rcnn = mask_rcnn_class(img)
        self.retina = retina_class(img)
        self.thread_pool = QThreadPool()

        self.retina_preds = []
        self.yolo_preds = []
        self.mask_preds = []

    def predict(self):
        self.retina.signals.bboxes.connect(self.get_retina_preds)
        self.thread_pool.start(self.retina)

        # self.darknet.signals.bboxes.connect(self.get_yolo_preds)
        # self.thread_pool.start(self.darknet)

        # self.mask_rcnn.signals.bboxes.connect(self.get_mask_preds)
        # self.thread_pool.start(self.mask_rcnn)



    def get_yolo_preds(self, preds):
        print(preds)
        print("Here!")

    def get_mask_preds(self, preds):
        print(preds)
        print("Here!")

    def get_retina_preds(self, preds):
        print(preds)
        print("Here!")