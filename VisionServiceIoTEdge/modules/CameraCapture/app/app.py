import io
import json
import requests
from flask import Flask, request, Response
from packages.ImageStream import ImageStream

image_stream = None

def create_app(test_config=None):
    global image_stream

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    @app.route("/camera/start", methods=["POST"])
    def initialize():
        global image_stream

        try:
            if not image_stream:
                image_stream = ImageStream()
                return Response("Camera instance has been created")
            else:
                return Response("Camera instance already exists")
        except Exception as e:
            return str(e), 500

    @app.route("/camera/stop", methods=["POST"])
    def close():
        global image_stream

        try:
            if not image_stream:
                return Response("Camera has not been initialized")
            elif image_stream.camera.closed:
                return Response("Camera is already closed")
            elif image_stream != None:
                image_stream.close()
                image_stream = None
                return Response("Success")
            else:
                return "Undefined method", 400
        except Exception as e:
            return str(e), 500

    @app.route("/image", methods=["GET"])
    def get_image():
        global image_stream

        try:
            image_stream.capture()
            bytes_io = io.BytesIO()
            image_stream.image.save(bytes_io, format="PNG")
            data = bytes_io.getvalue()

            return Response(data, mimetype="application/octet-stream")
        except Exception as e:
            return str(e), 500

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host='0.0.0.0')
