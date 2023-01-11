'''
MainWindow.py inherits QMainWindow class. QMainWindows is used to create the main screen
of the program UI. Toolbars, menus and... are created here. MainWindow executes mass detection algorithms
in seperate threads. Some functionality is not implemented yet and requesting them from UI results in termination of program.
'''




import sys
from PySide2.QtCore import Qt, Slot, QThreadPool
from PySide2.QtGui import QPainter, QIcon, QPixmap, QImageReader, QImage
from PySide2.QtWidgets import *
from PySide2.QtCharts import QtCharts
import pydicom
import cv2 
from retina_class import retina_class
from darknet.darknet_class import darknet_class
from mask_rcnn_class import mask_rcnn_class
import os
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        self.setWindowTitle("Breast Cancer Diagnosis")
        self.widget = widget
        self.setCentralWidget(self.widget)

        # Init variables
        self.init_instance_variables()
        # Init Actions
        self.init_actions()
        # Init Menu
        self.init_menus()
        # Init Toolbar
        self.init_toolbars()
        self.addToolBar(self.toolbar)
        # Init threadpool
        self.thread_pool = QThreadPool()

    def init_instance_variables(self):
        # img:
        self.cv2img = None
        self.qimage = None
        self.dcm_file = None
        # menu and toolbar
        self.menu = None
        self.file_menu = None
        self.predict_menu = None
        self.toolbar = None
        # actions
        self.open_action = None
        self.save_action = None
        self.save_as_action = None
        self.exit_action = None
        self.predict_action = None
        self.clear_pred_action = None
        # Model Instances
        self.retina_instance = None
        self.yolov3_instance = None

    def init_actions(self):
        # Open QAction
        self.open_action = QAction(QIcon("./assets/file.svg"),"Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)

        # Save QAction
        self.save_action = QAction(QIcon("./assets/diskette.svg"), "Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)

        # Save as QAction
        self.save_as_action = QAction(QIcon("./assets/save_as2.svg"), "Save as", self)
        self.save_as_action.setIcon
        self.save_as_action.setShortcut("Ctrl+A+S")
        self.save_as_action.triggered.connect(self.save_file_as)

        # Predict QAction
        self.predict_action = QAction(QIcon("./assets/stethoscope.svg"), "Predict", self)
        self.predict_action.setShortcut("Ctrl+T")
        self.predict_action.triggered.connect(self.predict_cancer)

        # Add Ground truth QAction
        self.gt_action = QAction("Ground Truth", self)
        self.gt_action.setShortcut("Ctrl+g")
        self.gt_action.triggered.connect(self.load_ground_truth)

        # Clear Predictions QAction
        self.clear_pred_action = QAction(QIcon("./assets/clear2.svg"), "Clear", self)
        self.clear_pred_action.setShortcut("Ctrl+Y")
        self.clear_pred_action.triggered.connect(self.clear_pred)

        # Zoom In QAction
        self.zoom_in_action = QAction(QIcon("./assets/zoom-in2.svg"), "Zoom in", self)
        self.zoom_in_action.triggered.connect(self.zoom_in)

        # Zoom Out QAction
        self.zoom_out_action = QAction(QIcon("./assets/zoom-out3.svg"), "Zoom out", self)
        self.zoom_out_action.triggered.connect(self.zoom_out)

        # Pan QAction
        self.pan_action = QAction(QIcon("./assets/pan.svg"), "Pan", self)
        self.pan_action.setCheckable(True)
        self.pan_action.triggered.connect(self.pan)

        # Exit QAction
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.exit_app)

    def init_menus(self):
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.predict_menu = self.menu.addMenu("Predictions")
        self.view_menu = self.menu.addMenu("View")

        #Add actions to menu:
            #File Menu:
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.exit_action)
            #Predict Menu
        self.predict_menu.addAction(self.predict_action)
        self.predict_menu.addAction(self.clear_pred_action)
        self.predict_menu.addAction(self.gt_action)
            #View Menu:
        self.view_menu.addAction(self.zoom_in_action)
        self.view_menu.addAction(self.zoom_out_action)
        self.view_menu.addAction(self.pan_action)

    def init_toolbars(self):
        self.toolbar = QToolBar("Main Toolbar")
        #Add actions to toolbar:
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        self.toolbar.addAction(self.save_as_action)
        self.toolbar.addAction(self.predict_action)
        self.toolbar.addAction(self.clear_pred_action)
        self.toolbar.addAction(self.zoom_in_action)
        self.toolbar.addAction(self.zoom_out_action)
        self.toolbar.addAction(self.pan_action)
        self.toolbar.addAction(self.gt_action)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    @Slot()
    def load_ground_truth(self, checked):
        fileName = QFileDialog.getOpenFileName(self, "Open Image/Dicom", "./", "Image Files (*.png *.jpg *.bmp *.tif *.tiff);;Dicom files (*.dcm);;All files (*.*)")
        if "Dicom" in fileName[1]:
            dcm_file = pydicom.dcmread(fileName[0])
            cv2img = dcm_file.pixel_array
            from byte_scale import bytescaling
            x_, y_ = cv2img.shape
            if(x_ <= y_):
                new_x = 2000
                new_y = y_ * new_x // x_
            else:
                new_y = 2000
                new_x = x_ * new_y // y_
            cv2img = cv2.resize(cv2img, (new_y, new_x), interpolation=cv2.INTER_AREA)
            cv2img = bytescaling(cv2img)  
            import skimage.color
            if cv2img.ndim != 3:
                cv2img = skimage.color.gray2rgb(cv2img)
            self.widget.add_mask_image(cv2img.copy())
        elif "Image" in fileName[1]:
            cv2img = cv2.imread(fileName[0])
            shape_ = cv2img.shape
            x_ = shape_[0]
            y_ = shape_[1]
            if(x_ <= y_):
                new_x = 2000
                new_y = y_ * new_x // x_
            else:
                new_y = 2000
                new_x = x_ * new_y // y_
            cv2img = cv2.resize(cv2img, (new_y, new_x), interpolation=cv2.INTER_AREA)
            self.widget.add_mask_image(cv2img.copy())
        elif fileName[1] == "":
            pass
        else:
            self.disp_message("File format not supported.")
        # pass

    @Slot()
    def open_file(self, checked):
        fileName = QFileDialog.getOpenFileName(self, "Open Image/Dicom", "./", "Image Files (*.png *.jpg *.bmp *.tif *.tiff);;Dicom files (*.dcm);;All files (*.*)")
        if "Dicom" in fileName[1]:
            dcm_file = pydicom.dcmread(fileName[0])
            self.cv2img = dcm_file.pixel_array
            from byte_scale import bytescaling
            x_, y_ = self.cv2img.shape
            if(x_ <= y_):
                new_x = 2000
                new_y = y_ * new_x // x_
            else:
                new_y = 2000
                new_x = x_ * new_y // y_
            print(self.cv2img.shape)
            self.cv2img = cv2.resize(self.cv2img, (new_y, new_x), interpolation=cv2.INTER_AREA)
            self.cv2img = bytescaling(self.cv2img)  
            import skimage.color
            if self.cv2img.ndim != 3:
                self.cv2img = skimage.color.gray2rgb(self.cv2img)
            self.qimage = QImage(self.cv2img, self.cv2img.shape[1], self.cv2img.shape[0],QImage.Format.Format_RGB888)
            if(self.qimage is None):
                self.disp_message("Couldn't load image")
            self.widget.set_main_image(self.qimage, self.cv2img.copy())
            self.widget.masks = []
        elif "Image" in fileName[1]:
            self.cv2img = cv2.imread(fileName[0])
            reader = QImageReader(fileName[0])
            reader.setAutoTransform(True)
            self.qimage = reader.read()
            if(self.qimage is None):
                self.disp_message("Couldn't load image")
            # cv2.imshow("S", self.cv2img)
            self.widget.set_main_image(self.qimage, self.cv2img.copy())
            self.widget.masks = []
        elif fileName[1] == "":
            pass
        else:
            self.disp_message("File format not supported.")
        # pass


    def disp_message(self, message_):
        msg_box = QMessageBox()
        msg_box.setText(message_)
        msg_box.exec()

    @Slot()
    def save_file(self, checked):
        QApplication.quit()
        # pass

    @Slot()
    def save_file_as(self, checked):
        QApplication.quit()
        #pass

    @Slot()
    def predict_cancer(self, checked):
        model_name = str(self.widget.select_model_combo_box.currentText())
        cancer_type =  str(self.widget.select_irregularity_combo_box.currentText())
        if cancer_type == "Mass" and model_name == "Retinanet":
            self.retina_instance = retina_class(np.copy(self.cv2img))
            self.retina_instance.signals.img.connect(self.disp_detected_image)
            self.thread_pool.start(self.retina_instance)
        elif cancer_type == "Mass" and model_name == "YOLOv3":
            self.yolov3_instance = darknet_class(np.copy(self.cv2img))
            self.yolov3_instance.signals.img.connect(self.disp_detected_image)
            self.thread_pool.start(self.yolov3_instance)

        elif cancer_type == "Mass" and model_name == "Mask RCNN":
            self.mask_rcnn_instance = mask_rcnn_class(np.copy(self.cv2img))
            self.mask_rcnn_instance.signals.img.connect(self.disp_detected_image)
            self.thread_pool.start(self.mask_rcnn_instance)

    @Slot()
    def clear_pred(self, checked):
        QApplication.quit()
        # pass

    def disp_detected_image(self, img):
        self.widget.add_image_tab_main_image_view(QImage(img, img.shape[1], img.shape[0],QImage.Format.Format_RGB888))

    @Slot()
    def zoom_in(self):
        self.widget.main_image_zoom_in()

    @Slot()
    def zoom_out(self):
        self.widget.main_image_zoom_out()

    @Slot()
    def pan(self):
        if(self.widget.scroll_area.is_waiting_pan):
            self.pan_action.setChecked(False)
        else:
            self.pan_action.setChecked(True)

        self.widget.toggle_pan()
