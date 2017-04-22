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

from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap


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

        preview = self.camera.capture_preview()

        label = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(preview)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()
