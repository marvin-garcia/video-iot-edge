import os
import sys
import png
import time
import PIL
from PIL import Image
from queue import Queue
from threading import Thread
from datetime import datetime
from picamera import PiCamera
from picamera.array import PiRGBArray

class VideoStream:

    def __init__(self, queue_size: int = 10):
        try:
            # NOTE: do not use RGB as image format, it messes up with the RaspberryPi camera
            self.stopped = False
            self.camera = PiCamera()
            self.Q = Queue(maxsize=queue_size)

        except Exception as e:
            print(str(e))
            self.close()

    def start(self, width=640, height=480, framerate=32):
        """Start a thread to read frames from the video stream"""

        try:
            t = Thread(target=self._capture, args=(width, height, framerate))
            t.daemon = True
            t.start()

            return self

        except Exception as e:
            raise e

    def stop(self):
        self.stopped = True

    def read(self):
        return self.Q.get()

    def more(self):
        return self.Q.qsize() > 0

    def _capture(self, width=640, height=480, framerate=32, format="rgb"):
        try:
            self.camera.resolution = (width, height)
            self.camera.framerate = framerate
            raw_capture = PiRGBArray(self.camera, size=(width, height))

            # allow the camera to warmup
            time.sleep(0.1)

            while not self.stopped:
                for frame in self.camera.capture_continuous(raw_capture, format=format, use_video_port=True):

                    if self.stopped:
                        break

                    # grab the raw NumPy array representing the image, then convert it to a PIL image object
                    image = self._convert_image(frame.array)
                    self.Q.put(image)

                    raw_capture.truncate(0)
                    # time.sleep(delay)

        except Exception as e:
            self.close()
            raise e

    def _convert_image(self, image_array: numpy.ndarray, mode: str = "L") -> PIL.Image.Image:
        try:
            # using numpy: self.image = png.from_array(image_array, mode=mode)
            image = Image.fromarray(image_array)
            return image

        except Exception as e:
            print(str(e))
            raise e

    def save_frame(self, path: str, date_format="%y%m%d%H%M%S%f"):
        """Start a thread to save framesfrom queue to disk"""

        try:
            t = Thread(target=self._save_frame, args=(path, date_format))
            t.daemon = True
            t.start()

            return self

        except Exception as e:
            raise e

    def _save_frame(self, path: str, date_format):
        try:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

            if self.more():
                while self.more():
                    image = self.read()
                    image.save("%s/img-%s.png" % (path, datetime.now().strftime(date_format)))

        except Exception as e:
            print(str(e))
            return False

    def close(self) -> bool:
        try:
            self.stop()
            self.camera.close()
            return True

        except Exception as e:
            print(str(e))
            return False
