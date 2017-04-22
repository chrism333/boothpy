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

import gphoto2 as gp


class Camera:

    def __init__(self):
        pass

    def open(self):
        try:
            context = gp.Context()
            camera = gp.Camera()
            camera.init(context)
            text = camera.get_summary(context)
            print('Summary')
            print('=======')
            print(str(text))
            camera.exit(context)

            self.context = context
            self.camera = camera

        except gp.GPhoto2Error as ex:
            return False

        return True

    def close(self):
        try:
            self.camera.exit(self.context)
        except gp.GPhoto2Error as ex:
            return False

        return True

    def capture_preview(self):
        self.camera.capture_preview(self.context)