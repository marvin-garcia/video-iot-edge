# Image Analyzer module

The Image Analyzer is a Python [module](./main.py) does the following:

- Calls the [CameraCapture](../CameraCapture/README.md) module via HTTP to receive an image
- Calls an [ImageClassifier](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/overview) module to for image classification
- If the image classification request returns any tags of interest, the image is stored in a local storage blob using the [StorageBlob](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-store-data-blob?view=iotedge-2018-06) module
- The tags are sent to a [StreamAnalytics]() module for further processing



The image capture frequency can be adjusted using the environment variable `CAPTURE_INTERVAL`, which is measured in seconds.