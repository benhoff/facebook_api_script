import sys
import os
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.NOTSET)
log.addHandler(sh)

from PyQt5 import QtGui, QtCore, QtWidgets

def size_hint():
    return QtCore.QSize(800, 400)

class ImageCropper(QtCore.QObject):
    def __init__(self, parent=None):
        super(ImageCropper, self).__init__(parent)
        file_path = os.path.dirname(os.path.realpath(__file__))
        self.cropped_photos_path = os.path.join(file_path, 'cropped_photos')
        if not os.path.exists(self.cropped_photos_path):
            os.mkdir(self.cropped_photos_path)

    @QtCore.pyqtSlot(QtCore.QFile, QtCore.QRect)
    def rect_slot(self, file_info, rectangle_info):
        full_image = QtGui.QImage(file_info.fileName())
        cropped_image = full_image.copy(rectangle_info)
        base_name = os.path.basename(file_info.fileName())
        base_name.replace('.', '_cropped.', 1)
        cropped_image.save(os.path.join(self.cropped_photos_path, base_name))


class MyGraphicScene(QtWidgets.QGraphicsScene):
    rect_signal = QtCore.pyqtSignal(QtCore.QFile, QtCore.QRect)
    resize_signal = QtCore.pyqtSignal(int, int)
    def __init__(self, picture_directory=None, parent=None):
        super(MyGraphicScene, self).__init__(parent)
        log.debug(picture_directory)
        if picture_directory is not None:
            self.pictures_list = os.listdir(picture_directory)
            # change to the absolute path
            self.pictures_list = [os.path.join(picture_directory, x) for x in self.pictures_list]
            log.debug(self.pictures_list)
            # Get rid of face_coordinates.txt if in list
            if 'face_coordinates.txt' in self.pictures_list:
                self.pictures_list.pop(self.pictures_list.index('face_coordinates.txt'))
            self.pixmap_item = None
            self.pixmap_filename = None

            self._next_image_helper()

        self.initial_radius = 5
        self.current_ellipse = None
        self._ellipse_upper_left_x = None
        self._ellipse_upper_left_y = None
        self._ellipse_width = None
        self._ellipse_height = None
        self._mouse_pressed = False
        self._x = None
        self._y = None

    def _next_image_helper(self):
        if self.pixmap_item is not None:
            self.removeItem(self.pixmap_item)
        self.pixmap_filename = QtCore.QFile(self.pictures_list.pop())
        log.debug(self.pixmap_filename.fileName())
        image = QtGui.QImage(self.pixmap_filename.fileName())
        pixmap = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(image))
        self.pixmap_item = self.addItem(pixmap)

    def send_rectangle_slot(self):
        self.rect_signal.emit(
                self.pixmap_filename,
                QtCore.QRect(self._ellipse_upper_left_x,
                self._ellipse_upper_left_y,
                self._ellipse_width,
                self._ellipse_height))

        self._next_image_helper()
                            

    def mousePressEvent(self, mouse_event):
        if self.current_ellipse is not None and not mouse_event.buttons() == QtCore.Qt.RightButton:
            self.removeItem(self.current_ellipse)
            self.current_ellipse = None

        self._mouse_pressed = True
        if mouse_event.buttons() == QtCore.Qt.LeftButton:
            self._ellipse_upper_left_x = mouse_event.scenePos().x()
            self._ellipse_upper_left_y = mouse_event.scenePos().y()
            self._ellipse_height = self.initial_radius * 2
            self._ellipse_width = self.initial_radius * 2

            self.current_ellipse = self.addRect(
                    mouse_event.scenePos().x(),
                    mouse_event.scenePos().y(),
                    self._ellipse_width,
                    self._ellipse_height)
        elif mouse_event.buttons() == QtCore.Qt.RightButton:
            self._x = mouse_event.scenePos().x()
            self._y = mouse_event.scenePos().y()


        #self.current_ellipse.setBrush(QtCore.Qt.white)
        super(MyGraphicScene, self).mousePressEvent(mouse_event)

    def mouseMoveEvent(self, mouse_event):
        if self._mouse_pressed and mouse_event.buttons() == QtCore.Qt.LeftButton:
            mouse_x = mouse_event.scenePos().x()
            mouse_y = mouse_event.scenePos().y()
            self._ellipse_width = abs(mouse_x - self._ellipse_upper_left_x)
            self._ellipse_height = abs(mouse_y - self._ellipse_upper_left_y)
            if mouse_x < self._ellipse_upper_left_x:
                self._ellipse_upper_left_x = mouse_x
            if mouse_y < self._ellipse_upper_left_y:
                self._ellipse_upper_left_y = mouse_y

            self.current_ellipse.setRect(
                    self._ellipse_upper_left_x,
                    self._ellipse_upper_left_y,
                    self._ellipse_width,
                    self._ellipse_height)

        elif self._mouse_pressed and mouse_event.buttons() == QtCore.Qt.RightButton and self.current_ellipse is not None:
            self._ellipse_upper_left_x = self._ellipse_upper_left_x - (self._x - mouse_event.scenePos().x())
            self._ellipse_upper_left_y =self._ellipse_upper_left_y - (self._y - mouse_event.scenePos().y())
            self._x = mouse_event.scenePos().x()
            self._y = mouse_event.scenePos().y()
            self.current_ellipse.setRect(
                    self._ellipse_upper_left_x,
                    self._ellipse_upper_left_y,
                    self._ellipse_width,
                    self._ellipse_height)

        super(MyGraphicScene, self).mouseMoveEvent(mouse_event)

    def mouseReleaseEvent(self, mouse_event):
        self._mouse_pressed = False

# Create QApplicaiton and main window
app = QtWidgets.QApplication(sys.argv)
main_window = QtWidgets.QMainWindow()
#main_window.sizeHint = size_hint




file_dir = os.path.dirname(os.path.realpath(__file__))
picture_directory= os.path.join(file_dir, 'pictures', '')
# Create scene
scene = MyGraphicScene(picture_directory)
image_cropper = ImageCropper()
scene.rect_signal.connect(image_cropper.rect_slot)

# create graphics view
graphics_view = QtWidgets.QGraphicsView()
graphics_view.setScene(scene)
scene.resize_signal.connect(graphics_view.resize)

widget = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()
push_button = QtWidgets.QPushButton('Finished Cropping!')
push_button.clicked.connect(scene.send_rectangle_slot)

# FIXME: Implement
#scene.rect_signal.connect(

layout.addWidget(graphics_view)
layout.addWidget(push_button)
widget.setLayout(layout)
main_window.setCentralWidget(widget)
main_window.show()
sys.exit(app.exec_())

"""
im= Image.open('C:/Users/1368170069A/swdev/image_editor/test.BMP')
im.show()
"""
