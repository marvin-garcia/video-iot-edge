import png
import time
import PIL
import numpy
from PIL import Image
from picamera import PiCamera
from picamera.array import PiRGBArray

class ImageStream:

    def image(self) -> PIL.Image.Image:
        pass

    def __init__(self, format="rgb"):
        try:
            self.__format = format
            self.camera = PiCamera()

        except Exception as e:
            print(str(e))
            self.close()

    def _capture(self, width=1280, height=720) -> numpy.ndarray:
        try:
            self.camera.resolution = (width, height)
            raw_capture = PiRGBArray(self.camera)

            # allow the camera to warmup
            time.sleep(0.1)

            self.camera.capture(raw_capture, format=self.__format)
            image_array = raw_capture.array

            return image_array

        except Exception as e:
            print(str(e))
            self.close()

    def _convert(self, image_array: numpy.ndarray, mode: str = "L") -> bool:
        try:
            # using numpy: self.image = png.from_array(image_array, mode=mode)
            self.image = Image.fromarray(image_array)
            return True

        except Exception as e:
            print(str(e))
            return False

    def capture(self, path: str = None) -> bool:
        try:
            array = self._capture()
            self._convert(array)

            if path:
                self.save(path)

            return True

        except Exception as e:
            print(str(e))
            return False

    def save(self, path: str) -> bool:
        try:
            self.image.save(path)
            return True

        except Exception as e:
            print(str(e))
            return False

    def close(self) -> bool:
        try:
            self.camera.close()
            return True

        except Exception as e:
            print(str(e))
            return False
