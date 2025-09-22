

import time
import colorsys
from datetime import datetime, timedelta

from govee import GoveeClient



APIKEY = "Go find me"



class HappyGlow:
    COLOR_CYCLE = [
        [255,   0,   0],
        [255,  64,   0],
        [255, 128,   0],
        [255, 192,   0],
        [255, 255,   0],
        [192, 255,   0],
        [128, 255,   0],
        [ 64, 255,   0],
        [  0, 255,  64],
        [  0, 255, 128],
        [  0, 255, 192],
        [  0, 255, 255],
        [  0, 192, 255],
        [  0, 128, 255],
        [  0,  64, 255],
        [  0,   0, 255]

    ]
    THRESHOLD = .95

    def __init__(self, apikey):
        self.client = GoveeClient(APIKEY)
        self.start_time = None
        self.end_time = None
        self.full_duration = None
        self.fixture = None


    def set_start_time(self, start_time):
        self.start_time = start_time
        self.set_duration()

    def set_end_time(self, end_time):
        self.end_time = end_time
        self.set_duration()

    def set_duration(self):
        if self.start_time is not None and self.end_time is not None:
            self.full_duration =(self.end_time - self.start_time).total_seconds()


    def set_luminosity(self):
        now = datetime.now()
        if now < self.start_time or now > self.end_time:
            self.turn_off()
            return
        current_seconds = now - self.start_time
        offset = float(current_seconds) / float(self.full_duration)
        if offset < self.THRESHOLD:
            self.fixture.set_brightness(0.1)
        else:
            self.fixture.set_brightness(1.0)

        lighting_index = offset * len(self.COLOR_CYCLE)
        self.set_color(self.COLOR_CYCLE[lighting_index])

    def set_color(self, color):
        self.fixture.set_color(color)

    def turn_off(self):
        self.fixture.set_brightness(0.0)

    def connect_to_fixture(self, somespec):
        pass


def cycle_colors(device_mac, cycle_duration_minutes=5):
    """
    Cycles a Govee RGB bulb through the color spectrum.

    Args:
        device_mac (str): The MAC address of the Govee bulb.
        cycle_duration_minutes (int): The total time in minutes for one full color cycle.
    """
    client = GoveeClient(APIKEY)

    try:
        with GoveeLedStrip(device_mac) as strip:
            print(f"Connected to Govee bulb: {device_mac}")
            print("Starting color cycle. Press Ctrl+C to stop.")

            while True:
                elapsed_time = time.time() - start_time
                progress = (elapsed_time % cycle_duration_seconds) / cycle_duration_seconds

                # Use HSV color space for a smooth transition through the spectrum
                # Hue (progress) determines the color, Saturation and Value are max
                rgb = colorsys.hsv_to_rgb(progress, 1.0, 1.0)

                # Convert RGB values from 0-1 range to 0-255 range
                red = int(rgb[0] * 255)
                green = int(rgb[1] * 255)
                blue = int(rgb[2] * 255)

                strip.set_color((red, green, blue))

                # A short delay to prevent overwhelming the device with commands
                time.sleep(0.5)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure the MAC address is correct and the device is reachable.")

def main():
    controller = HappyGlow(APIKEY)
    controller.connect_to_fixture(somespec)
    now = datetime.now()
    controller.set_start_time(now)
    endtime = now + timedelta(hours=8)
    controller.set_end_time(endtime)
    while now < endtime:
        time.sleep(1000)
        controller.set_luminosity()
        now = datetime.now()



if __name__ == '__main__':
    main()
