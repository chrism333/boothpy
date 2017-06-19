# Copyright 2017 Christian Menard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import QTimer, Qt


class ErrorMessage(QMessageBox):

    def __init__(self, error, description):
        super().__init__()
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle('PyBooth Error')
        self.setText(error)
        self.setInformativeText(description)


class BoothPyWidget(QWidget):

    def __init__(self, camera):
        super().__init__()

        self.camera = camera

        # store the desktop geometry
        self.dg = QApplication.desktop().screenGeometry()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('BoothPy')

        self.preview = QLabel(self)
        self.preview.setGeometry(self.dg)
        self.preview.setStyleSheet(
                'QLabel { background-color : black; color : black; }')
        self.preview.setAlignment(Qt.AlignCenter)

        self.preview_frame_timer = QTimer()
        self.preview_frame_timer.timeout.connect(self.on_preview_frame_timeout)
        self.preview_frame_timer.setInterval(50)

        self.display_image_timer = QTimer()
        self.display_image_timer.timeout.connect(self.on_display_image_timeout)

        self.showFullScreen()
        self.enable_preview()

    def enable_preview(self):
        self.preview_frame_timer.start()

    def disable_preview(self):
        self.preview_frame_timer.stop()

        # switch to black frame
        pixmap = QPixmap(self.dg.width(), self.dg.height())
        pixmap.fill(QColor(0, 0, 0))
        self.show_pixmap(pixmap)

    def on_preview_frame_timeout(self):
        preview_data = None

        # Stop the timer and restart after capturing the preview frame.
        # If w don't stop the timer, we and up with multiple error messages
        # on preview timeout.
        self.preview_frame_timer.stop()

        try:
            preview_data = self.camera.capture_preview()
        except BaseException as e:
            self.disable_preview()
            err = ErrorMessage('Error while capturing preview:', str(e))
            self.close()
            err.exec_()

        self.preview_frame_timer.start()

        pixmap = QPixmap()
        if preview_data is not None:
            pixmap.loadFromData(preview_data)
        self.show_pixmap(pixmap)

    def on_display_image_timeout(self):
        self.enable_preview()

    def show_pixmap(self, pixmap):
        scaled = pixmap.scaled(self.dg.width(),
                               self.dg.height(),
                               Qt.KeepAspectRatio,
                               transformMode=Qt.SmoothTransformation)
        self.preview.setPixmap(scaled)
        self.repaint()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()

        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Space:
            self.disable_preview()

            try:
                image_path = self.camera.capture_image()
                pixmap = QPixmap()
                pixmap.load(image_path)
                self.show_pixmap(pixmap)

                self.display_image_timer.start(2000)
            except BaseException as e:
                err = ErrorMessage('Error while capturing image:', str(e))
                self.close()
                err.exec_()
