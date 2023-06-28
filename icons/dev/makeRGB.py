import sys
from PIL import Image
import json
class RGBMaker:
    def __init__(self, filename):
        self.filename = filename
        self.width = None
        self.height = None

    def frame_to_rgb(self, frame, background_value=0):
        # Convert the frame image to RGBA mode
        rgba_frame = frame.convert("RGBA")

        # Get the dimensions of the frame
        width, height = rgba_frame.size

        # Create an empty list to store the RGB565 pixel values
        rgb565_data = []

        # Iterate over each pixel in the frame
        for y in range(height):
            for x in range(width):
                # Get the RGBA values of the pixel in the frame
                r, g, b, a = rgba_frame.getpixel((x, y))

                # Replace the background color with the provided background value
                if a == 0:
                    r, g, b = background_value, background_value, background_value

                # Convert the RGB values to RGB565 format
                rgb565 = ((r & 0b11111000) << 8) | ((g & 0b11111100) << 3) | (b >> 3)

                # Append the RGB565 value to the list
                rgb565_data.append(rgb565)

        return rgb565_data

    def clean_frame(self, frame):
        # Clean the frame to ensure all frames have the same size and black background
        cleaned_frame = Image.new("RGBA", frame.size, (0, 0, 0))
        cleaned_frame.paste(frame, (0, 0), frame)
        return cleaned_frame

    def make_rgb(self, background_value=0):
        # Open the GIF image
        try:
            gif_image = Image.open(self.filename)
        except IOError:
            print(f"Error: Unable to open '{self.filename}'. Please make sure it is a valid GIF image.")
            return []


        # Create an empty list to store the RGB565 pixel values
        rgb565_data_frames = []

        self.width, self.height = gif_image.size

        # Iterate over each frame in the GIF image
        try:
            while True:
                # Get the current frame
                frame = gif_image.convert("RGBA")

                # Clean the frame to ensure all frames have the same size and black background
                cleaned_frame = self.clean_frame(frame)

                # Convert the cleaned frame to RGB565 format
                rgb565_data = self.frame_to_rgb(cleaned_frame, background_value)

                # Append the current frame's RGB565 data to the list of frames
                rgb565_data_frames.append(rgb565_data)

                # Move to the next frame
                gif_image.seek(gif_image.tell() + 1)

        except EOFError:
            pass

        return rgb565_data_frames
    def print_color_palette_from_data(self, data, background_value=0):
        print("Color Palette From Data:")
        unique_colors = set(data)  # Get unique colors

        # Add the background value to the unique colors set
        unique_colors.add(background_value)

        # Count the occurrences of each color
        color_counts = {color: data.count(color) for color in unique_colors}

        for rgb565 in unique_colors:
            # Extract the RGB components from RGB565 format
            r = (rgb565 >> 8) & 0xF8
            g = (rgb565 >> 3) & 0xFC
            b = (rgb565 << 3) & 0xF8

            # Convert the RGB components to hexadecimal
            hex_value = "0x{:04X}".format(rgb565)

            # Format the columns for alignment
            swatch_col = "\033[48;2;{};{};{}m  \033[0m".format(r, g, b)
            rgb565_col = "{:<7}".format(rgb565)
            hex_col = "{:<9}".format(hex_value)
            count_col = "{:<5}".format(color_counts[rgb565])

            # Print the color information, count, and ASCII swatch
            print("Swatch: {} RGB565: {} Hex: {} Count: {}".format(swatch_col, rgb565_col, hex_col, count_col))
        print("\n")

    def print_color_palette_from_image(self):
        # Open the image file
        try:
            image = Image.open(self.filename)
        except IOError:
            print(f"Error: Unable to open '{self.filename}'. Please make sure it is a valid image.")
            return

        # Check if the image has a color palette
        if image.mode == "P":
            # Get the color palette
            palette = image.getpalette()

            print("Color Palette From Image:")
            unique_colors = set()

            # Iterate over the palette and extract unique colors
            for i in range(0, len(palette), 3):
                # Get the RGB values
                r, g, b = palette[i: i + 3]

                # Convert RGB to RGB565 format
                rgb565 = ((r & 0b11111000) << 8) | ((g & 0b11111100) << 3) | (b >> 3)

                # Add the RGB565 value to the set of unique colors
                unique_colors.add(rgb565)

            # Print the unique colors and their ASCII swatches
            self.print_color_palette_from_data(unique_colors)
        else:
            print("The image does not have a color palette.")

    def replace(self, data, old_value, new_value):
        # Replace the old value with the new value in the data list
        return [new_value if value == old_value else value for value in data]

    def print_ascii_swatches(self, rgb565_data):
        print("ASCII Swatches:")

        for y in range(self.height):
            for x in range(self.width):
                rgb565 = rgb565_data[y * self.width + x]

                # Extract the RGB components from RGB565 format
                r = (rgb565 >> 8) & 0b11111000
                g = (rgb565 >> 3) & 0b11111100
                b = (rgb565 << 3) & 0b11111000

                # Normalize the RGB components to the range of 0-255
                r = (r | (r >> 5)) & 0xFF
                g = (g | (g >> 6)) & 0xFF
                b = (b | (b >> 5)) & 0xFF

                # Determine the ANSI color code based on the RGB components
                ansi_color_code = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)

                # Print the ANSI color escape sequence and a space to represent the swatch
                print("\033[48;5;{}m  \033[0m".format(ansi_color_code), end="")

            print()  # Move to the next line after printing each row

    # def print_rgb565_data(self, rgb565_data):
    #     print("RGB565 Data ({}x{}):".format(self.width, self.height))
    #
    #     max_value_length = len(str(max(rgb565_data)))  # Calculate the maximum length of RGB565 values
    #
    #     for i in range(0, len(rgb565_data), self.width):
    #         row = rgb565_data[i: i + self.width]
    #         row_str = ", ".join(["{:{}}".format(value, max_value_length) for value in row])
    #         if i < len(rgb565_data) - self.width:
    #             row_str += ","
    #         print(row_str)

    def print_rgb565_data(self, rgb565_data, colors=True):
        print("RGB565 Data ({}x{}):".format(self.width, self.height))

        max_value_length = len(str(max(rgb565_data)))  # Calculate the maximum length of RGB565 values

        color_escapes = {
            0b00000: '\033[30m',  # Black
            0b00001: '\033[34m',  # Blue
            0b00100: '\033[32m',  # Green
            0b00101: '\033[36m',  # Cyan
            0b10000: '\033[31m',  # Red
            0b10001: '\033[35m',  # Magenta
            0b10100: '\033[33m',  # Yellow
            0b11111: '\033[37m'  # White
        }

        for i in range(0, len(rgb565_data), self.width):
            row = rgb565_data[i: i + self.width]
            row_str = ""

            for value in row:
                value_str = "{:{}}".format(value, max_value_length)

                if colors:
                    # Extract the RGB components from RGB565 format
                    r = ((value & 0b1111100000000000) >> 11) << 3
                    g = ((value & 0b0000011111000000) >> 5) << 2
                    b = (value & 0b0000000000111110) << 3

                    # Determine the text color based on the RGB565 value
                    if value == 0:
                        color_escape = color_escapes[0]
                    else:
                        color_escape = "\033[38;2;{};{};{}m".format(r, g, b)

                    value_str = "{}{}{}".format(color_escape, value_str, '\033[0m')

                row_str += value_str + ", "

            row_str = row_str.rstrip(", ")

            if i < len(rgb565_data) - self.width:
                row_str += ","
            print(row_str)

    def generate_test_data(self, rgb565_data):
        test_data = {
            "stack": False,
            "draw": [
                {
                    "db": [
                        0, 0, self.width, self.height,
                        rgb565_data
                    ]
                }
            ]
        }
        return test_data
def main():
    if len(sys.argv) < 2:
        print("Please provide the filenames of the GIF images.")
        sys.exit(1)

    gif_filenames = sys.argv[1:]

    for gif_filename in gif_filenames:
        rgb_maker = RGBMaker(gif_filename)

        # Call the make_rgb function with the GIF filename
        rgb565_data_frames = rgb_maker.make_rgb()

        if not rgb565_data_frames:
            continue

        frame_count = len(rgb565_data_frames)

        # Print the color palette and RGB565 data for each frame
        print(f"--- Color Palette and RGB565 Data for {gif_filename} ---")

        for frame_index, rgb565_data in enumerate(rgb565_data_frames):
            print(f"Frame {frame_index + 1} of {frame_count}:")
            rgb_maker.print_color_palette_from_data(rgb565_data)
            rgb_maker.print_ascii_swatches(rgb565_data)

            print(f"--- Raw Data for Frame {frame_index + 1} of {frame_count} ---")
            rgb_maker.print_rgb565_data(rgb565_data, colors=True)

            # Generate the test data dictionary for the frame
            test_data = rgb_maker.generate_test_data(rgb565_data)
            test_data_json = json.dumps(test_data)

            print("--- Test Data JSON for Frame {frame_index + 1} of {frame_count} ---")
            print(test_data_json)
            print()


if __name__ == "__main__":
    main()