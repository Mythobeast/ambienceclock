

import time
import colorsys
from govee_led_we import GoveeLedStrip


def cycle_colors(device_mac, cycle_duration_minutes=5):
    """
    Cycles a Govee RGB bulb through the color spectrum.

    Args:
        device_mac (str): The MAC address of the Govee bulb.
        cycle_duration_minutes (int): The total time in minutes for one full color cycle.
    """
    if not device_mac:
        print("Error: Please provide the MAC address of your Govee bulb.")
        return

    try:
        with GoveeLedStrip(device_mac) as strip:
            print(f"Connected to Govee bulb: {device_mac}")
            print("Starting color cycle. Press Ctrl+C to stop.")

            strip.set_power(True)
            strip.set_brightness(1.0)

            start_time = time.time()
            cycle_duration_seconds = cycle_duration_minutes * 60

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


if __name__ == '__main__':
    # !!! IMPORTANT !!!
    # REPLACE "XX:XX:XX:XX:XX:XX" WITH YOUR GOVEE BULB'S MAC ADDRESS
    GOVEE_MAC_ADDRESS = "XX:XX:XX:XX:XX:XX"

    # You can change the duration of a full color cycle (in minutes)
    CYCLE_DURATION = 5

    cycle_colors(GOVEE_MAC_ADDRESS, CYCLE_DURATION)
