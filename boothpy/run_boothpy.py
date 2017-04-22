#!/usr/bin/env python3

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

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

from boothpy.widget import BoothPyWidget
from boothpy.camera import Camera

# terminate on signals, e.g., SIGTERM
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    cam = Camera()

    ret = cam.open()

    if not ret:
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle('Error')
        error_dialog.setText('Error while opening your camera! ' +
                             'Is a camera connected?')
        error_dialog.show()
        sys.exit(app.exec_())

    w = BoothPyWidget(cam)

    ret = cam.close()

    if not ret:
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle('Error')
        error_dialog.setText('Error while closing your camera!')
        error_dialog.show()

    sys.exit(app.exec_())
