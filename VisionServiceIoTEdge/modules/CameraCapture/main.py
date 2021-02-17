# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import io
import os
import sys
import json
import time
import asyncio
import requests
from PIL import Image
from six.moves import input
from threading import Thread
from src.ImageStream import ImageStream
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

COUNT=0
CAPTURE_INTERVAL=5

async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "IoT Hub Client for Python" )

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()

        # define behavior for receiving an input message on input1
        async def input1_listener(module_client):
            while True:
                input_message = await module_client.receive_message_on_input("input1")  # blocking call
                print("the data in the message received on input1 was ")
                print(input_message.data)
                print("custom properties are")
                print(input_message.custom_properties)
                print("forwarding mesage to output1")
                await module_client.send_message_to_output(input_message, "output1")

        # define behavior for halting the application
        def stdin_listener():
            while True:
                try:
                    selection = input("Press Q to quit\n")
                    if selection == "Q" or selection == "q":
                        print("Quitting...")
                        break
                except:
                    time.sleep(10)

        # define behavior for receiving direct methods
        def device_method_listener(device_client):
            global CAPTURE_INTERVAL

            while True:
                method_request = device_client.receive_method_request()
                print (
                    "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                        method_name=method_request.name,
                        payload=method_request.payload
                    )
                )
                if method_request.name == "SetCaptureInterval":
                    try:
                        CAPTURE_INTERVAL = int(method_request.payload)
                    except ValueError:
                        response_payload = {"Response": "Invalid parameter"}
                        response_status = 400
                    else:
                        response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                        response_status = 200
                else:
                    response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
                    response_status = 404

                method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
                device_client.send_method_response(method_response)

        # Schedule task for C2D Listener
        listeners = asyncio.gather(input1_listener(module_client))

        print ( "The sample is now waiting for messages. ")

        # Start a thread to listen for direct methods
        device_method_thread = Thread(target=device_method_listener, args=(module_client,))
        device_method_thread.daemon = True
        device_method_thread.start()

        # Run the stdin listener in the event loop
        loop = asyncio.get_event_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        # Run endless loop for recurring tasks
        global COUNT
        print("Count: %s" % COUNT)
        COUNT += 1
        time.sleep(CAPTURE_INTERVAL)

        # Wait for user to indicate they are done listening for messages
        await user_finished

        # Cancel listening
        listeners.cancel()

        # Finally, disconnect
        await module_client.disconnect()

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    asyncio.run(main())