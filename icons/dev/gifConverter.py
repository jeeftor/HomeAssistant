import sys
import os
from PIL import Image


class GifConverter:
    """
    A class that converts a GIF image into SVG files and generates Markdown file referencing the SVG files as images.
    """

    DEFAULT_CELL_SIZE = 16

    def __init__(self, gif_path: str, output_dir: str, cell_size: int):
        """
        Initializes the GifConverter class.

        Args:
            gif_path (str): Path to the GIF image.
            output_dir (str): Output directory for the SVG files and Markdown file.
            cell_size (int): Size of each cell in the SVG representation.
        """
        self.gif_path = gif_path
        self.output_dir = output_dir
        self.cell_size = cell_size
        self.base_name = os.path.splitext(os.path.basename(self.gif_path))[
            0
        ]  # Extract base name
        self.gif = None

    def convert_to_svg(self) -> list[str]:
        """
        Converts the GIF image to a series of SVG files.

        Returns:
            list[str]: List of file paths to the generated SVG files.
        """
        # Open the GIF image
        self.gif = Image.open(self.gif_path)

        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Get the base name of the input file
        base_name = os.path.splitext(os.path.basename(self.gif_path))[0]

        # Convert each frame to SVG
        svg_file_paths = []
        for frame_index in range(self.gif.n_frames):
            # Select the current frame
            self.gif.seek(frame_index)
            frame = self.gif.convert("RGBA")

            # Get the dimensions of the frame
            width, height = frame.size

            # Calculate the cell size
            if self.cell_size is None:
                self.cell_size = self.DEFAULT_CELL_SIZE

            # Create an SVG file path for the current frame
            svg_path = os.path.join(
                self.output_dir, f"{base_name}_frame_{frame_index}.svg"
            )
            svg_file_paths.append(svg_path)

            # Open the SVG file
            with open(svg_path, "w") as svg_file:
                # Write the SVG header
                svg_file.write(
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * self.cell_size}" height="{height * self.cell_size}">\n'
                )

                # Write SVG rectangles for each pixel
                for y in range(height):
                    for x in range(width):
                        # Get the color of the current pixel
                        r, g, b, a = frame.getpixel((x, y))

                        # Check if the pixel is transparent or matches the background color
                        if a == 0 or (r, g, b, a) == self.gif.info.get(
                            "background", ()
                        ):
                            # Set the pixel color to black
                            r, g, b = 0, 0, 0

                        # Convert RGB values to hexadecimal
                        hex_color = f"#{r:02x}{g:02x}{b:02x}"

                        # Calculate the position and size of the SVG rectangle
                        rect_x = x * self.cell_size
                        rect_y = y * self.cell_size
                        rect_width = self.cell_size
                        rect_height = self.cell_size

                        # Write the SVG rectangle for the current pixel
                        svg_file.write(
                            f'<rect x="{rect_x}" y="{rect_y}" width="{rect_width}" height="{rect_height}" fill="{hex_color}" />\n'
                        )

                # Write the SVG footer
                svg_file.write("</svg>\n")

            print(f"SVG file '{svg_path}' has been created successfully.")

        return svg_file_paths

    def generate_markdown(self, svg_file_paths: list[str]) -> None:
        """
        Generates a Markdown file with image references to the SVG files.

        Args:
            svg_file_paths (list[str]): List of file paths to the SVG files.
        """
        markdown_path = os.path.join(self.output_dir, f"{self.base_name}.md")

        with open(markdown_path, "w") as markdown_file:
            # Write the Markdown syntax for each SVG file as an image tag with a title
            for frame_index, svg_file_path in enumerate(svg_file_paths):
                image_name = f"{self.base_name}_frame_{frame_index}.svg"
                title = f"Frame {frame_index}"
                markdown_file.write(f'![{title}]({image_name} "{title}")\n')

        print(f"Markdown file '{markdown_path}' has been created successfully.")

    def gif_to_html(self) -> None:
        """
        Converts the GIF image to an HTML file.

        Args:
            gif_path (str): Path to the GIF image.
            cell_size (int): Size of each cell in the HTML table.
        """
        # Open the GIF image
        gif = Image.open(self.gif_path)

        # Generate the output HTML file path
        output_path = os.path.join(self.output_dir, f"{self.base_name}.html")

        # Create the HTML file
        with open(output_path, "w") as html_file:
            # Write the HTML header
            html_file.write("<html>\n")
            html_file.write("<body>\n")

            # Iterate over each frame in the GIF
            for frame_index in range(gif.n_frames):
                # Select the current frame
                gif.seek(frame_index)
                frame = gif.convert("RGBA")

                # Get the dimensions of the frame
                width, height = frame.size

                # Calculate the cell size
                if self.cell_size is None:
                    cell_size = GifConverter.DEFAULT_CELL_SIZE

                # Write the frame number as the title
                html_file.write(f"<h3>Frame Number: {frame_index}</h3>\n")

                # Write the table start tag
                html_file.write('<table border="0" cellpadding="0" cellspacing="0">\n')

                # Iterate over each pixel in the frame
                for y in range(height):
                    # Write the table row start tag
                    html_file.write("<tr>\n")
                    for x in range(width):
                        # Get the color of the current pixel
                        r, g, b, a = frame.getpixel((x, y))

                        # Check if the pixel is transparent or matches the background color
                        if a == 0 or (r, g, b, a) == gif.info.get("background", ()):
                            # Set the pixel color to black
                            r, g, b = 0, 0, 0

                        # Convert RGB values to hexadecimal
                        hex_color = f"#{r:02x}{g:02x}{b:02x}"

                        # Write the table cell with the updated pixel color
                        html_file.write(
                            f'<td style="background-color:{hex_color};width:{self.cell_size}px;height:{self.cell_size}px;"> </td>\n'
                        )

                    # Write the table row end tag
                    html_file.write("</tr>\n")

                # Write the table end tag
                html_file.write("</table>\n")

                # Add a line break between frames
                html_file.write("<br>\n")

            # Write the HTML footer
            html_file.write("</body>\n")
            html_file.write("</html>\n")

        print(f'HTML file "{output_path}" has been created successfully.')


def main() -> None:
    """
    Main function for executing the GIF to SVG conversion and generating Markdown and HTML files.
    """
    if len(sys.argv) < 2:
        print("Please provide the path to the GIF image.")
        return

    gif_path = sys.argv[1]
    cell_size = None
    if len(sys.argv) >= 3:
        cell_size = int(sys.argv[2])

    converter = GifConverter(gif_path, "output", cell_size)
    svg_file_paths = converter.convert_to_svg()
    converter.generate_markdown(svg_file_paths)
    converter.gif_to_html()


if __name__ == "__main__":
    main()
