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

import os
import sys
import argparse
from PyQt5.QtWidgets import QApplication

from boothpy.widget import BoothPyWidget, ErrorMessage
from boothpy.camera import Camera
from boothpy.camera import DummyCamera

# terminate on signals, e.g., SIGTERM
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', type=str, default='/tmp',
                        help='Set the directory where captured images should' +
                             'be stored. Default is /tmp')
    parser.add_argument('-t', '--try-mode', action='store_true', default=False,
                        help='start without connecting to a camera')
    parser.add_argument('-r', '--raw', action='store_true', default=False,
                        help='capture and store raw (works only if the camera is setup to raw+jpeg)')

    args = parser.parse_args()

    app = QApplication(sys.argv)

    if args.try_mode:
        cam = DummyCamera(args)
    else:
        cam = Camera(args)

    if not os.path.isdir(args.directory):
        raise RuntimeError('Output directory %s does not exist!' %
                           args.directory)

    try:
        cam.open()
    except BaseException as e:
        err = ErrorMessage('Error while opening your Camera:', str(e))
        err.show()
        sys.exit(app.exec_())

    w = BoothPyWidget(cam)

    try:
        cam.close()
    except BaseException as e:
        err = ErrorMessage('Error while closing your Camera:', str(e))
        err.show()
        sys.exit(app.exec_())

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
