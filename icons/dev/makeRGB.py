import sys
from PIL import Image


class RGBMaker:
    def __init__(self, filename):
        self.filename = filename
        self.width = None
        self.height = None

    def make_rgb(self, background_value=0):
        # Open the GIF image
        gif_image = Image.open(self.filename)

        # Convert the image to RGBA mode to access the alpha channel
        rgba_image = gif_image.convert("RGBA")

        # Get the dimensions of the image
        self.width, self.height = rgba_image.size

        # Create an empty list to store the RGB565 pixel values
        rgb565_data = []

        # Iterate over each pixel in the image
        for y in range(self.height):
            for x in range(self.width):
                # Get the RGBA values of the pixel
                r, g, b, a = rgba_image.getpixel((x, y))

                # Replace the background color with the provided background value
                if a == 0:
                    r, g, b = background_value, background_value, background_value

                # Convert the RGB values to RGB565 format
                rgb565 = ((r & 0b11111000) << 8) | ((g & 0b11111100) << 3) | (b >> 3)

                # Append the RGB565 value to the list
                rgb565_data.append(rgb565)

        return rgb565_data
    def print_color_palette_from_data(self, data, background_value=0):
        print("Color Palette From Data:")
        unique_colors = set(data)  # Get unique colors

        # Add the background value to the unique colors set
        unique_colors.add(background_value)

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

            # Print the color information and ASCII swatch
            print("Swatch: {} RGB565: {} Hex: {}".format(swatch_col, rgb565_col, hex_col))
        print("\n")

    def print_color_palette_from_image(self):
        # Open the image file
        image = Image.open(self.filename)

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

    def print_rgb565_data(self, rgb565_data):
        print("RGB565 Data ({}x{}):".format(self.width, self.height))

        max_value_length = len(str(max(rgb565_data)))  # Calculate the maximum length of RGB565 values

        for i in range(0, len(rgb565_data), self.width):
            row = rgb565_data[i: i + self.width]
            row_str = ", ".join(["{:{}}".format(value, max_value_length) for value in row])
            if i < len(rgb565_data) - self.width:
                row_str += ","
            print(row_str)


def main():
    if len(sys.argv) < 2:
        print("Please provide the filename of the GIF image.")
        sys.exit(1)

    gif_filename = sys.argv[1]
    rgb_maker = RGBMaker(gif_filename)

    # Call the make_rgb function with the GIF filename
    rgb565_data = rgb_maker.make_rgb()

    # Replace specific values if desired
    # replace_values = {19967: 19967, 65535: 65535, 8223: 8223}
    # for old_value, new_value in replace_values.items():
    #     rgb565_data = rgb_maker.replace(rgb565_data, old_value, new_value)

    rgb_maker.print_color_palette_from_data(rgb565_data)
    # rgb_maker.print_color_palette_from_image()
    rgb_maker.print_ascii_swatches(rgb565_data)
    rgb_maker.print_rgb565_data(rgb565_data)


if __name__ == "__main__":
    main()
