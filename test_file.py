import zmq

def main():
    context = zmq.Context()
    print("Connecting to the NASA image microservice...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    socket.send_string("Fetch a random NASA image")

    filename = socket.recv_string()
    if filename.startswith("ERROR:"):
        print(filename)
        return

    socket.send(b"ACK")

    image_data = socket.recv()

    with open(filename, "wb") as file:
        file.write(image_data)

    print(f"NASA image saved as: {filename}")

if __name__ == "__main__":
    main()
