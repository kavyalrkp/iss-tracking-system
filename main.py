import requests
import time
import json
import datetime
import turtle
import os


def get_astros_data(api_url: str = "http://api.open-notify.org/astros.json"):
    data = requests.get(api_url).json()

    if data['message'] == 'success':
        with open('iss-astros.json', 'w') as iss_file:
            json.dump(data, iss_file, indent=4)
            # Optional to open the file in browser.
            # webbrowser.open('iss-astros.json')

        print(f"There are currently {data['number']} people on the ISS.")
        for person in data['people']:
            print(f"{person['name']} is currently on the ISS, Craft: {person['craft']}")

    else:
        print('Failed to obtain astronauts data.')


def get_iss_turtle(resolution: tuple = (1280, 720)):
    # Setup the world map in turtle module
    screen = turtle.Screen()
    screen.setup(*resolution)
    screen.setworldcoordinates(-180, -90, 180, 90)

    # Load the world map image
    world_map_path = os.path.join(os.path.dirname(__file__), 'images', 'world-map.gif')
    iss_icon_path = os.path.join(os.path.dirname(__file__), 'images', 'iss-icon.gif')

    if not os.path.exists(world_map_path):
        raise FileNotFoundError(f"World map image not found at path: {world_map_path}")
    if not os.path.exists(iss_icon_path):
        raise FileNotFoundError(f"ISS icon image not found at path: {iss_icon_path}")

    screen.bgpic(world_map_path)
    screen.register_shape(iss_icon_path)
    iss = turtle.Turtle()
    iss.shape(iss_icon_path)
    iss.setheading(45)
    iss.penup()

    return iss


def update_position(iss: turtle.Turtle,
                    api_url: str = "http://api.open-notify.org/iss-now.json",
                    sleep_duration: int = 5):

    while True:
        # Load the current status of the ISS in real-time
        try:
            data = requests.get(api_url).json()
        except Exception as e:
            print(e)
            update_position(iss, api_url, sleep_duration)

        if data['message'] == 'success':
            # Extract the ISS location
            location = data["iss_position"]
            latitude = float(location['latitude'])
            longitude = float(location['longitude'])

            print(f"\nCurrent coordinates Latitude: {latitude}, Longitude: {longitude}")
            print(f"Current time: {datetime.datetime.fromtimestamp(data['timestamp'])}")

            # Update the ISS turtle object location on the map
            iss.goto(longitude, latitude)
            iss.pendown()

            # Refresh each sleep duration seconds
            time.sleep(sleep_duration)

        else:
            print("Failed to obtain ISS position data.")


def main():
    get_astros_data()
    iss_turtle = get_iss_turtle()
    update_position(iss_turtle)


if __name__ == "__main__":
    main()
