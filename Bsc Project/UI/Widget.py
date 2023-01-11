'''
Widget is a QQWidget and defines program layouts and widgets. Widget is assigned to MainWindow and this class handles Program appearence.
'''

import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from PySide2.QtGui import QPixmap, QPalette, QGuiApplication, QImage
from ScrollArea import ScrollArea
import numpy as np
import skimage.color
import cv2

class Widget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.preds = []
        self.img = None
        self.cv2img = None
        self.dcm = None
        self.scale_factor = 1
        self.create_layouts()
        self.setLayout(self.main_layout)
        self.create_left_description_layout_widgets()
        # self.create_edit_image_layout_widgets()
        self.create_view_image_layout_widgets()
        self.masks = []
        
    def create_layouts(self):
       
        self.main_layout = QVBoxLayout()
        self.content_layout = QHBoxLayout()
       
        self.left_description_layout = QVBoxLayout()
        self.left_description_layout.setAlignment(Qt.AlignTop)
        # self.left_description_frame = QFrame(self)
        self.image_layout = QVBoxLayout()
        self.image_layout.setAlignment(Qt.AlignLeft)

        self.main_layout.addLayout(self.content_layout)
        
        self.content_layout.addLayout(self.left_description_layout)
        # self.content_layout.addWidget(self.image_view_tab)
        

    def create_left_description_layout_widgets(self):
        # Combobox used for selecting model
        self.select_model_combo_box_label = QLabel("Select Model")
        self.select_model_combo_box = QComboBox(self)
        self.select_model_combo_box.addItem("YOLOv3")
        self.select_model_combo_box.addItem("Retinanet")
        self.select_model_combo_box.addItem("Mask RCNN")
        self.select_model_combo_box.addItem("Ensemble of Models")
        
        # Combobox used to select Mass and or Calcification
        self.select_irregularity_combo_box_label = QLabel("Select type of Irregularities")
        self.select_irregularity_combo_box = QComboBox(self)
        self.select_irregularity_combo_box.addItem("Mass")
        self.select_irregularity_combo_box.addItem("Calcification")
        self.select_irregularity_combo_box.addItem("All")
        
        # Slider defining confidence threshold used for detecting mass
        self.select_confidence_slider_label = QLabel("Select Confidence threshold")
        self.select_confidence_slider = QSlider(Qt.Horizontal)
        
        # Size Policy
        self.select_model_combo_box_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.select_model_combo_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.select_confidence_slider_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.select_confidence_slider.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.select_irregularity_combo_box_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.select_irregularity_combo_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Add above widgets to layout
        self.left_description_layout.addWidget(self.select_model_combo_box_label)
        self.left_description_layout.addWidget(self.select_model_combo_box)
        self.left_description_layout.addWidget(self.select_confidence_slider_label)
        self.left_description_layout.addWidget(self.select_confidence_slider)
        self.left_description_layout.addWidget(self.select_irregularity_combo_box_label)
        self.left_description_layout.addWidget(self.select_irregularity_combo_box)
    
    def create_view_image_layout_widgets(self):
        
        pixmap = QPixmap('./assets/backg.jpg')
        pixmap = pixmap.scaled(pixmap.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.image_view_tab = QTabWidget()
        self.main_image_label = QLabel("image")
        self.main_image_label.setBackgroundRole(QPalette.Base)
        self.main_image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.main_image_label.setScaledContents(True)
        self.main_image_label.setPixmap(pixmap)
        self.main_image_label.resize(pixmap.size())
        self.main_image_label.setMouseTracking(True)
        self.scroll_area = ScrollArea()
        self.scroll_area.setMouseTracking(True)
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.main_image_label)
        self.scroll_area.setVisible(True)
        self.preds.append([0, self.main_image_label, 1, self.scroll_area])
        self.image_layout.addWidget(self.scroll_area)
        widget = QWidget()
        widget.setLayout(self.image_layout)

        self.image_view_tab.addTab(widget, "Case")
        self.content_layout.addWidget(self.image_view_tab)
    def set_main_image(self, qimage, cv2img=None):
        pixmap = QPixmap()
        pixmap = pixmap.fromImage(qimage)
        self.main_image_label.setPixmap(pixmap)
        self.main_image_label.resize(pixmap.size())
        if cv2img is not None:
            self.cv2img = cv2img
            size_img = self.cv2img.shape
            # x_, y_ = size_img[0], size_img[1]
            # if(x_ <= y_):
            #     new_x = 800
            #     new_y = y_ * new_x // x_
            # else:
            #     new_y = 800
            #     new_x = x_ * new_y // y_
            # print(self.cv2img.shape)
            # self.cv2img = cv2.resize(self.cv2img, (new_y, new_x), interpolation=cv2.INTER_AREA)

    def add_mask_image(self, mask_img):
        mask_img = mask_img.astype(np.bool)
        # if mask_img.ndim != 3:
        #         mask_img = skimage.color.gray2rgb(mask_img)
        self.masks.append(mask_img)
        self.cv2img = self.apply_mask(self.cv2img, mask_img, (0, 255, 0))
        qimage = QImage(self.cv2img, self.cv2img.shape[1], self.cv2img.shape[0],QImage.Format.Format_RGB888)
        self.set_main_image(qimage)
        for i, pred in enumerate(self.preds):
            if i > 0:
                [_, image_label, _, _] = pred
                pixmap = image_label.pixmap()

                channels_count = 4
                image = pixmap.toImage()
                
                # s = image.constBits().asstring(pixmap.width() * pixmap.height() * channels_count)
                s = image.constBits()
                arr = np.array(s).reshape((pixmap.height(), pixmap.width(), channels_count))
                arr = arr[:, :, 0:3].copy()
                print(arr.shape)
                arr = self.apply_mask(arr, mask_img, (0, 255, 0))
                qimage = QImage(arr, arr.shape[1], arr.shape[0],QImage.Format.Format_RGB888)
                pixmap = QPixmap(qimage)
                image_label.setPixmap(pixmap)
                image_label.resize(pixmap.size())

    def main_image_zoom_in(self):
        self.scale_image(1.25)
    
    def main_image_zoom_out(self):
        self.scale_image(0.8)

    def main_image_normal_size(self):
        self.main_image_label.adjustSize()
        self.scale_factor = 1

    def main_image_fitToWindow(self):
        self.scroll_area.setWidgetResizable(True)
        self.main_image_normal_size()

    def scale_image(self, scale):
        idx = self.image_view_tab.currentIndex()
        pred_idx = -1
        for i in range(len(self.preds)):
            if self.preds[i][0] == idx:
                pred_idx = i
        # for i in range(self.image_view_tab.currentWidget().layout().count()):
        #     scroll_area = self.image_view_tab.currentWidget().layout().itemAt(i).widget()
        #     if scroll_area is None:
        #         print("ASDAKSDADSds")
        #     else:
        #         break
        self.preds[pred_idx][2] = self.preds[pred_idx][2] * scale
        self.preds[pred_idx][1].resize(self.preds[pred_idx][2] * self.preds[pred_idx][1].pixmap().size())
        vertical_scroll_bar = self.preds[pred_idx][3].horizontalScrollBar()
        horizontal_scroll_bar = self.preds[pred_idx][3].verticalScrollBar()
        vertical_scroll_bar.setValue(int(scale * vertical_scroll_bar.value()+ ((scale - 1) * vertical_scroll_bar.pageStep()/2)))
        horizontal_scroll_bar.setValue(int(scale * horizontal_scroll_bar.value()+ ((scale - 1) * horizontal_scroll_bar.pageStep()/2)))

    def toggle_pan(self):
        if not self.scroll_area.is_waiting_pan: 
            self.scroll_area.is_waiting_pan = True
            self.scroll_area.setCursor(Qt.OpenHandCursor)
        else:
            self.scroll_area.is_waiting_pan = False
            self.scroll_area.setCursor(Qt.ArrowCursor)

    def add_image_tab_main_image_view(self, qimage):
        i = len(self.preds)+1
        pixmap = QPixmap()
        pixmap = pixmap.fromImage(qimage)
        pixmap = pixmap.scaled(pixmap.size(), Qt.KeepAspectRatio, Qt.FastTransformation)


        for mask_img in self.masks:
            channels_count = 4
            image = pixmap.toImage()
            s = image.constBits()
            arr = np.array(s).reshape((pixmap.height(), pixmap.width(), channels_count))
            arr = arr[:, :, 0:3].copy()
            print(arr.shape)
            arr = self.apply_mask(arr, mask_img, (0, 255, 0))
            qimage = QImage(arr, arr.shape[1], arr.shape[0],QImage.Format.Format_RGB888)
            pixmap = QPixmap(qimage)



        main_image_label = QLabel("prediction"+str(i))
        main_image_label.setBackgroundRole(QPalette.Base)
        main_image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        main_image_label.setScaledContents(True)
        main_image_label.setPixmap(pixmap)
        main_image_label.resize(pixmap.size())
        main_image_label.setMouseTracking(True)
        scroll_area = ScrollArea()
        scroll_area.setMouseTracking(True)
        scroll_area.setBackgroundRole(QPalette.Dark)
        scroll_area.setAlignment(Qt.AlignCenter)
        scroll_area.setWidget(main_image_label)
        scroll_area.setVisible(True)
        self.preds.append([i, main_image_label, 1, scroll_area])
        # scroll_area.setWidgetResizable(True)
        image_layout = QVBoxLayout()
        image_layout.addWidget(scroll_area)
        widget = QWidget()
        widget.setLayout(image_layout)
        # resize
        
        # w = pixmap.width()
        # h = pixmap.height()

        # while(scroll_area.width() < w or scroll_area.height() < h):

        #     self.main_image_zoom_out()
        #     self.image_view_tab.children()
        #     w = w * self.scale_factor
        #     h = h * self.scale_factor

        self.image_view_tab.addTab(widget, "prediction"+str(i-1))
        self.image_view_tab.setCurrentIndex(self.image_view_tab.count()-1)



    def apply_mask(self, image, mask, color, alpha=0.5):
        """Apply the given mask to the image.
        """

        mask = mask[:, :, 0]
        for c in range(3):
            image[:, :, c] = np.where(mask == 1,
                                    image[:, :, c] *
                                    (1 - alpha) + alpha * color[c] * 255,
                                    image[:, :, c])
        return image