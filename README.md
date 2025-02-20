# NASA Image Generator Microservice

This is a microservice that fetches random space-themed images from NASA's Image Library.
Images are returned as binary files so that they can be used as backgrounds.

## Prerequisites
Microservice A has been written in Python, and it uses **ZeroMQ** to send and receive data from two Python files that are independent of each other. In order to start the microservice, you must have Python installed on your computer. When you run the following code, you will start the microservice:
```
python microservice.py
```
The microservice listens on localhost:5555

## A. How to REQUEST Data

In order to send a request, you must first connect to the microservice using **ZeroMQ** on localhost:5555. 
You can either send an empty string as the request message, or you can send any string (e.g. "Fetch Random NASA image)
No other parameters are needed

### Example call:
```python
# set up zeromq
context = zmq.Context()

# you can include a message here if you'd like
print("Connecting to the NASA image microservice...")

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# send the request message
socket.send_string("Fetch a random NASA image")
```

## B. How to RECEIVE Data

After sending the request, the microservice will senf back the filename of the image as a string. You then need to acknowledge the microservice so that it knows to send the binary image data. After that, the microservice sends the image as binary data and can be saved to a file.

### Example call:
```python
# receive the filename
filename = socket.recv_string()
print(f"Filename received: {filename}")

# send acknowledgement
socket.send(b"ACK")

# receive binary image data and save image as a file
image_data = socket.recv()

with open(filename, "wb") as file:
    file.write(image_data)

print(f"Random image saved as: {filename}")
```

## C. UML Sequence Diagram
