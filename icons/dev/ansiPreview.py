import requests
import time
from PIL import Image, ImageDraw
from typing import List
import asyncio
import sys
import os


class ScreenCapture:
    def __init__(
        self,
        endpoint_url: str,
        width: int,
        height: int,
        initial_duration: int,
    ) -> None:
        self.endpoint_url = endpoint_url
        self.width = width
        self.height = height
        self.initial_duration = initial_duration

    async def capture_frame(self) -> None:
        """Capture a frame from the endpoint and display a live preview."""
        frame_count = 0
        while True:
            response = requests.get(self.endpoint_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Get the RGB565 color values as a list
                rgb565_values = response.json()

                # Create a new PIL image of the original dimensions (32x8)
                image = Image.new("RGB", (self.width, self.height))
                draw = ImageDraw.Draw(image)

                # Set the color of each pixel in the image
                for y in range(self.height):
                    for x in range(self.width):
                        # Convert the decimal RGB565 value to RGB888
                        rgb565 = rgb565_values[y * self.width + x]
                        red = (rgb565 & 0xFF0000) >> 16
                        green = (rgb565 & 0x00FF00) >> 8
                        blue = rgb565 & 0x0000FF

                        # Draw a pixel with the converted RGB value
                        draw.point((x, y), fill=(red, green, blue))

                # Scale the image to the desired dimensions (256x64)
                scaled_image = image.resize(
                    (self.width * 4, self.height * 4), resample=Image.NEAREST
                )

                # Print the frame count and live preview
                self.print_live_preview(frame_count, image)

                frame_count += 1

            await asyncio.sleep(0.05)  # Delay between frame captures

    def print_live_preview(self, frame_count: int, image: Image.Image) -> None:
        """Print the live preview of the image, clearing the console screen."""
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\033[32mFrames Shown: {frame_count}\033[0m")
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                sys.stdout.write(f"\033[48;2;{r};{g};{b}m  \033[0m")
            sys.stdout.write("\n")
        print("\033[32mctrl+c to exit\033[0m")


async def capture_loop(screen_capture: ScreenCapture) -> None:
    await screen_capture.capture_frame()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Awtrix Clock Screen Capture")
    parser.add_argument(
        "--ip",
        type=str,
        help="The IP address of your Awtrix Clock",
    )

    args = parser.parse_args()

    # Prompt user for the IP address if not provided through command line argument
    if args.ip is None:
        endpoint_ip = input("What is the IP for your Awtrix Clock: ")
    else:
        endpoint_ip = args.ip

    # Endpoint URL
    endpoint_url = f"http://{endpoint_ip}/api/screen"

    # Image dimensions
    width = 32
    height = 8

    # GIF parameters
    initial_duration = 50  # in milliseconds

    # Create ScreenCapture instance
    screen_capture = ScreenCapture(endpoint_url, width, height, initial_duration)

    # Create the event loop
    loop = asyncio.get_event_loop()

    # Run the capture loop
    try:
        loop.run_until_complete(capture_loop(screen_capture))
    except KeyboardInterrupt:
        pass

    # Close the event loop
    loop.close()


if __name__ == "__main__":
    main()
