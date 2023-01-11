'''
QScrollArea is the widget used for displaying image in UI. This class provides zoom, pan, dragging scrolling and etc. functionality.
'''


from PySide2.QtWidgets import QScrollArea
from PySide2.QtCore import Qt, QPoint, QTimer
import time

HOLD_MIDDLE_THRESHOLD = 0.2

class ScrollArea(QScrollArea):

    def __init__(self):
        QScrollArea.__init__(self)
        self.is_dragging = False
        self.is_waiting_pan = False
        self.drag_using_middle_button = False
        self.middle_press_point = QPoint()
        self.time_holding_middle_button = 0
        self.last_drag_pos = QPoint()
        self.setMouseTracking(True)
    def mousePressEvent(self, mouse_event):
        if self.drag_using_middle_button:
            self.drag_using_middle_button = False
            self.setCursor(Qt.ArrowCursor)
        else:
            if(mouse_event.button() == Qt.RightButton):
                if self.is_waiting_pan:
                    self.is_waiting_pan = False
                    self.setCursor(Qt.ArrowCursor)
                else:
                    self.is_dragging = True
                    self.last_drag_pos = mouse_event.pos()
                    self.setCursor(Qt.ClosedHandCursor)
            elif mouse_event.button() == Qt.LeftButton and self.is_waiting_pan:
                self.is_dragging = True
                self.last_drag_pos = mouse_event.pos()
                self.setCursor(Qt.ClosedHandCursor)

            elif mouse_event.button() == Qt.MiddleButton:
                self.drag_using_middle_button = True
                self.time_holding_middle_button = time.time()
                self.middle_press_point = mouse_event.pos()
                self.setCursor(Qt.SizeAllCursor)
    def mouseReleaseEvent(self, mouse_event):
        if mouse_event.button() == Qt.MiddleButton:
            if(time.time() - self.time_holding_middle_button > HOLD_MIDDLE_THRESHOLD):
                self.drag_using_middle_button = False
                self.setCursor(Qt.ArrowCursor)

        else:
            self.is_dragging = False
            if not self.is_waiting_pan:
                self.setCursor(Qt.ArrowCursor)
            else:
                self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, mouse_event):
        if self.drag_using_middle_button:
            delta = 0.5*(-mouse_event.pos() + self.middle_press_point)
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()-delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value()-delta.y())

        if self.is_dragging:
            delta = mouse_event.pos() - self.last_drag_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()-delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value()-delta.y())
            self.last_drag_pos = mouse_event.pos()