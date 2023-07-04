What is here? (good question).

There are some helper scripts.

- `gifConverter.py`: This will take a `.gif` file and drop out a set of `.svg` files for each frame of the image. Additionaly it will make an `.html` and a `.md` file linking to those preview images

- `gifMaker.py`: You give this script an ip address (of your clock) - and it will record the screen frame by frame and write the result to `output.gif`. You also get a live ANSI preview in the command line.
- `makeRGB.py`: This script will take a set of `.gif` files as input and convert them into RGB565 format, as well as giving you various options (A macro or raw data to send to curl) to render the gif as a `draw` command.


- `ansiPreview.py` Mirrors an Awtrix screen to the CLI