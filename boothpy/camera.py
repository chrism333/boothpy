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
from shutil import copyfile


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
        self.camera.trigger_capture(self.context)

        raw_file_path = None
        jpeg_file_path = None
        while True:
            etype, value = self.camera.wait_for_event(1000, self.context)
            if etype == gp.GP_EVENT_FILE_ADDED:
                if raw_file_path is None and self.args.raw:
                    raw_file_path = value
                else:
                    print(value.name)
                    jpeg_file_path = value
                    break

        if raw_file_path is not None:
            raw_target = os.path.join(self.args.directory, raw_file_path.name)
            raw_camera_file = self.camera.file_get(raw_file_path.folder,
                                                   raw_file_path.name,
                                                   gp.GP_FILE_TYPE_NORMAL,
                                                   self.context)
            gp.check_result(gp.gp_file_save(raw_camera_file, raw_target))

        jpeg_target = os.path.join(self.args.directory, jpeg_file_path.name)
        jpeg_camera_file = self.camera.file_get(jpeg_file_path.folder,
                                                jpeg_file_path.name,
                                                gp.GP_FILE_TYPE_NORMAL,
                                                self.context)
        gp.check_result(gp.gp_file_save(jpeg_camera_file, jpeg_target))

        if os.path.splitext(jpeg_target)[1] == 'jpg' or \
           os.path.splitext(jpeg_target)[1] == 'JPG':
            return jpeg_target
        else:   # XXX on some cameras we get a JPEG first, then the raw_target
                # variable stores out jpeg
            return raw_target


class DummyCamera:

    def __init__(self, args):
        self.i = 0
        self.args = args

    def open(self):
        pass

    def close(self):
        pass

    def capture_preview(self):
        return None

    def capture_image(self):
        target = os.path.join(self.args.directory, 'test_%d.jpg' % self.i)
        self.i += 1
        copyfile('test.jpg', target)
        return 'test.jpg'
