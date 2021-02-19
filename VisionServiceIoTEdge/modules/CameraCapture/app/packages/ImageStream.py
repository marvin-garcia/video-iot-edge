import os
import sys
import png
import PIL
import time
import numpy
from PIL import Image
from queue import Queue
from threading import Thread
from datetime import datetime
from picamera import PiCamera
from picamera.array import PiRGBArray

class ImageStream:

    def image(self) -> PIL.Image.Image:
        pass

    def __init__(self, frame_queue_size: int=3):
        try:
            self.camera = PiCamera()
            
            # Frame settings
            self.frame_stopped = False
            self.Q = Queue(maxsize=frame_queue_size)

        except Exception as e:
            print(str(e))
            self.close()

    def __capture(self, width: int=1280, height: int=720, format: str="rgb") -> numpy.ndarray:
        try:
            self.camera.resolution = (width, height)
            raw_capture = PiRGBArray(self.camera)

            # allow the camera to warmup
            time.sleep(0.1)

            self.camera.capture(raw_capture, format=format)
            image_array = raw_capture.array

            return image_array

        except Exception as e:
            print(str(e))
            self.close()

    def __convert(self, image_array: numpy.ndarray, mode: str="L") -> bool:
        try:
            # using numpy: self.image = png.from_array(image_array, mode=mode)
            self.image = Image.fromarray(image_array)
            return True

        except Exception as e:
            print(str(e))
            return False

    def capture(self, width: int=1280, height: int=720, format: str="rgb", path: str = None) -> bool:
        try:
            array = self.__capture(width, height, format)
            self.__convert(array)

            if path:
                self.save_image(path)

            return True

        except Exception as e:
            print(str(e))
            return False

    def save_image(self, path: str) -> bool:
        try:
            self.image.save(path)
            return True

        except Exception as e:
            print(str(e))
            return False

    def set_frame_queue_size(self, size: int):
        try:
            self.Q = Queue(maxsize=size)

        except Exception as e:
            print(str(e))
            self.frame_stopped = True
            self.close()

    def start_frame(self, width: int=640, height: int=480, framerate: float=32, format: str="rgb"):
        """Start a thread to read frames from the video stream"""

        try:
            t = Thread(target=self.__capture_frame, args=(width, height, framerate, format))
            t.daemon = True
            t.start()

            return self

        except Exception as e:
            raise e

    def stop_frame(self):
        self.frame_stopped = True

    def read_frame(self) -> PIL.Image.Image:
        return self.Q.get()

    def more(self) -> bool:
        return self.Q.qsize() > 0

    def __capture_frame(self, width: int, height: int, framerate: float, format: int):
        try:
            self.camera.resolution = (width, height)
            self.camera.framerate = framerate
            raw_capture = PiRGBArray(self.camera, size=(width, height))

            # allow the camera to warmup
            time.sleep(0.1)

            while not self.frame_stopped:
                for frame in self.camera.capture_continuous(raw_capture, format=format, use_video_port=True):

                    if self.frame_stopped:
                        break

                    # grab the raw NumPy array representing the image, then convert it to a PIL image object
                    image = self.__convert_frame_image(frame.array)
                    self.Q.put(image)

                    raw_capture.truncate(0)
                    # time.sleep(delay)

        except Exception as e:
            self.close()
            raise e

    def __convert_frame_image(self, image_array: numpy.ndarray, mode: str="L") -> PIL.Image.Image:
        try:
            # using numpy: self.image = png.from_array(image_array, mode=mode)
            image = Image.fromarray(image_array)
            return image

        except Exception as e:
            print(str(e))
            raise e

    def save_frame(self, path: str, date_format: str="%y%m%d%H%M%S%f"):
        """Start a thread to save framesfrom queue to disk"""

        try:
            t = Thread(target=self.__save_frame, args=(path, date_format))
            t.daemon = True
            t.start()

            return self

        except Exception as e:
            raise e

    def __save_frame(self, path: str, date_format: str):
        try:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

            if self.more():
                while self.more():
                    image = self.read()
                    image.save("%s/img-%s.png" %
                            (path, datetime.now().strftime(date_format)))

        except Exception as e:
            print(str(e))
            return False

    def close(self) -> bool:
        try:
            self.stop_frame()
            self.camera.close()
            return True

        except Exception as e:
            print(str(e))
            return False
