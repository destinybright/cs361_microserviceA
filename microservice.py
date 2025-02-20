import zmq
import requests
import random
import os

NASA_IMAGE_API_URL = "https://images-api.nasa.gov/search"

# list of cool space words so that only cool space images are fetched
# ran into issue of other images being fetched
# feel free to add more keywords if you want, these were just ones that got me good results :)
COOL_KEYWORDS = [
    "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto",
    "black hole", "supernova", "comet", "galaxy", "nebula", "moon",
]

def get_image():
    # randomly choose a keyword from the cool ones
    cool_keyword = random.choice(COOL_KEYWORDS)
    params = {
        "q": cool_keyword,
        "media_type": "image"
    }
    
    try:
        # search for images using the random keyword
        response = requests.get(NASA_IMAGE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # get the list of image items
        items = data.get("collection", {}).get("items", [])

        # select random image
        random_item = random.choice(items)
        image_links = random_item.get("links", [])

        image_url = image_links[0].get("href", "")

        image_response = requests.get(image_url, stream=True)
        image_response.raise_for_status()
        filename = image_url.split("/")[-1]  

        return image_response.content, filename, None
    
    except requests.exceptions.RequestException as e:
        return None, None, f"Failed to fetch image: {str(e)}"

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP) 
    
    socket.bind("tcp://*:5555")

    while True:
        print("NASA image microservice running...")
        message = socket.recv_string() 
        print(f"Received request: {message}")

        image_data, filename, error = get_image()

        if error:
            socket.send_string(f"ERROR: {error}")
        else:
            socket.send_string(filename)
            socket.recv()

            socket.send(image_data)

if __name__ == "__main__":
    main()
