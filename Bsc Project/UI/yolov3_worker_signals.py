from PySide2.QtCore import Signal, QObject

class yolov3_worker_signals(QObject):

    img = Signal(object)
    bboxes = Signal(object)