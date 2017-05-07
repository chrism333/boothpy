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
import os


class Camera:

    def __init__(self, args):
        self.args = args

    def open(self):
        context = gp.Context()
        camera = gp.Camera()
        camera.init(context)

        config = camera.get_config(context)

        # find and check the image format config item
        ok, image_format = gp.gp_widget_get_child_by_name(config,
                                                          'imageformat')
        if ok >= gp.GP_OK:
            value = gp.check_result(gp.gp_widget_get_value(image_format))
            if value == 'raw':
                raise RuntimeError('Cannot preview raw images!')

        # find and set the capture size class config item
        # this is required for some canon cameras and does not hurt for others
        ok, capture_size_class = gp.gp_widget_get_child_by_name(
                config,
                'capturesizeclass')
        if ok >= gp.GP_OK:
            value = gp.check_result(gp.gp_widget_get_choice(capture_size_class,
                                                            2))
            gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
            gp.check_result(gp.gp_camera_set_config(camera, config, context))

        self.context = context
        self.camera = camera
        self.config = config

    def close(self):
        self.camera.exit(self.context)

    def capture_preview(self):
        camera_file = self.camera.capture_preview(self.context)
        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
        return memoryview(file_data)

    def capture_image(self):
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE, self.context)
        target = os.path.join(self.args.directory, file_path.name)
        camera_file = self.camera.file_get(file_path.folder,
                                           file_path.name,
                                           gp.GP_FILE_TYPE_NORMAL,
                                           self.context)
        gp.check_result(gp.gp_file_save(camera_file, target))
        return target
