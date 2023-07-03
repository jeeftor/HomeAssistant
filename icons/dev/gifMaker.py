import requests
import time
from PIL import Image, ImageDraw
from typing import List
import asyncio
import sys
import os
from datetime import timedelta


class ScreenCapture:
    def __init__(
        self,
        endpoint_url: str,
        width: int,
        height: int,
        gif_filename: str,
        initial_duration: int,
        max_duration: int,
    ) -> None:
        self.endpoint_url = endpoint_url
        self.width = width
        self.height = height
        self.gif_filename = gif_filename
        self.initial_duration = initial_duration
        self.max_duration = max_duration
        self.gif_frames: List[Image.Image] = []

    async def capture_frame(self) -> None:
        """Capture a frame from the endpoint and add it to the GIF frames."""
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

                # Add the current frame to the GIF
                self.gif_frames.append(scaled_image)
                frame_count += 1

                # Print the frame count and live preview
                self.print_live_preview(frame_count, image)

            await asyncio.sleep(0.05)  # Delay between frame captures

    def print_live_preview(self, frame_count: int, image: Image.Image) -> None:
        """Print the live preview of the image, clearing the console screen."""
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\033[32mFrames captured: {frame_count}\033[0m")
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                sys.stdout.write(f"\033[48;2;{r};{g};{b}m  \033[0m")
            sys.stdout.write("\n")

    def save_as_gif(self) -> None:
        """Save the captured frames as a GIF and print the duration."""
        if len(self.gif_frames) > 0:
            # Calculate the total duration of the GIF
            total_duration = len(self.gif_frames) * self.initial_duration

            # Save the frames as a GIF
            self.gif_frames[0].save(
                self.gif_filename,
                format="GIF",
                append_images=self.gif_frames[1:],
                save_all=True,
                duration=self.initial_duration,
                loop=0,
            )

            # Print the duration
            duration_str = str(timedelta(milliseconds=total_duration))
            print(f"\nGIF saved successfully. Duration: {duration_str}")
        else:
            print("\nNo frames captured. GIF not saved.")


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
    gif_filename = "output.gif"
    initial_duration = 50  # in milliseconds
    max_duration = 500  # in milliseconds

    # Create ScreenCapture instance
    screen_capture = ScreenCapture(
        endpoint_url, width, height, gif_filename, initial_duration, max_duration
    )

    # Prompt user to start capturing
    input("Press Enter to start capturing frames...")

    # Start time
    start_time = time.time()

    # Create the event loop
    loop = asyncio.get_event_loop()

    # Run the capture loop
    try:
        loop.run_until_complete(capture_loop(screen_capture))
    except KeyboardInterrupt:
        pass

    # Save frames as GIF
    screen_capture.save_as_gif()

    # End time
    end_time = time.time()

    # Calculate capture duration
    capture_duration = end_time - start_time
    print(f"Capture duration: {capture_duration:.2f} seconds")


if __name__ == "__main__":
    main()
