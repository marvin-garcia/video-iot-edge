# Camera Capture module

This module is optimized to run on a Raspberry Pi and use the Pi's camera module. You can see all its dependencies in the [Dockerfile.arm32v7](./Dockerfile.arm32v7) and [requirements.txt](./requirements.txt).



## Pre-requisites

The Raspberry Pi Camera is treated like any other Linux device and when attached, it is mounted at `/dev/vchiq`. By default, the camera device is only accessible by `pi` and `root` users. In order for the camera to be used from inside a Docker container, one must change its permissions first. Since Raspbian is a Debian-based Linux distribution, you can add rules to the `udev` system by running the code below:

```bash
# Provide right permissions to video devices
mkdir -p /etc/udev/rules.d/
echo 'SUBSYSTEM=="vchiq",MODE="0666"' > /etc/udev/rules.d/99-camera.rules
echo 'SUBSYSTEM=="vcsm-cma",MODE="0666"' >> /etc/udev/rules.d/99-camera.rules
```



The rule above grants read/write access to all users.



## IoT Edge module requirements

The section above covers how to allow all users to use the camera, but we still need to provide a way for the camera to be accessible from inside the Docker container when it gets launched with the IoT Edge deployment. This is accomplished in the `Create Option` section of your module definition in the [deployment file](../../deployment.template.json):

```json
"cameracapture": {
  "settings": {
    "createOptions": {
      "Hostname": "cameracapture",
      "HostConfig": {
        "Binds": [
          "/opt/vc:/opt/vc"
        ],
        "Devices": [
          {
            "PathOnHost": "/dev/vchiq",
            "PathInContainer": "/dev/vchiq",
            "CgroupPermissions": "rwm"
          },
          {
            "PathOnHost": "/dev/vcsm-cma",
            "PathInContainer": "/dev/vcsm-cma",
            "CgroupPermissions": "rwm"
          }
        ],
        ...
      }
    }
  },
  "env": {
    "LD_LIBRARY_PATH": {
      "value": "/opt/vc/lib"
    }
  },
  ...
}
```



A few things to note:

- Tools that use the Raspberry Pi Camera like [raspistill](https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md), [raspivid](https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md) and [PiCamera](https://picamera.readthedocs.io/en/release-1.13/) require several dependencies which are pre-installed in the `/opt/vc` folder. We make those dependencies accessible to the Docker container by mounting the folder in the same location using the `settings.createOptions.HostConfig.Binds` section.
- In the [docker run](https://docs.docker.com/engine/reference/commandline/run/) command, the option `--device` adds a host device to the container. We achieve the same result and mount both `/dev/vchiq` and `/dev/vcsm-cma` by adding them to the section `settings.createOptions.HostConfig.Devices`.
- Inside the `/opt/vc` directory is another directory called `lib` that contains some shared libraries. The easiest way to tell Linux to use this directory is by setting the environment variable `LD_LIBRARY_PATH=/opt/vc/lib`.
- The `Hostname` and `HostConfig` sections are required because the module runs a [Flask](https://flask.palletsprojects.com/en/1.1.x/) web application and needs to bee accessible through the internal network.



## How to interact with the Camera

The Python script [ImageStream](./app/packages/ImageStream.py) contains a class called `ImageStream` that leverages the Python module `PiCamera` to capture images and image frames. Feel free to play around with its methods.



## Wrapping it all together

Finally, the module runs a Flask application contained in the Python script [app.py](app/app.py) that contains three basic HTTP endpoints to initialize the camera, capture images and stop the camera instance object.