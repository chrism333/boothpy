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

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('BoothPy')

        self.preview = QLabel(self)
        self.preview.setGeometry(QApplication.desktop().screenGeometry())
        self.preview.setScaledContents(True)

        self.preview_frame_timer = QTimer()
        self.preview_frame_timer.timeout.connect(self.on_preview_frame_timeout)
        self.preview_frame_timer.setInterval(50)

        self.showFullScreen()
        self.enable_preview()

    def enable_preview(self):
        self.preview_frame_timer.start()

    def disable_preview(self):
        self.preview_frame_timer.stop()

        # switch to black frame
        pixmap = QPixmap(100, 100)
        pixmap.fill(QColor(0, 0, 0))
        self.preview.setPixmap(pixmap)
        self.repaint()

    def on_preview_frame_timeout(self):
        preview_data = None

        try:
            preview_data = self.camera.capture_preview()
        except BaseException as e:
            err = ErrorMessage('Error while capturing preview:', str(e))
            self.close()
            err.exec_()

        pixmap = QPixmap()
        pixmap.loadFromData(preview_data)
        self.preview.setPixmap(pixmap)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()

        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Space:
            self.disable_preview()

            try:
                self.camera.capture_image()
            except BaseException as e:
                err = ErrorMessage('Error while capturing image:', str(e))
                self.close()
                err.exec_()

            self.enable_preview()
