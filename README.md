# programation

programation stands for "**Progra**mmatic Ani**mation**", basically drawing
with a computer, but that sounded fancier. After watching videos from
[3blue1brown](https://www.3blue1brown.com/) I was inspired to make my own
animation toolkit, based on [his](https://github.com/3b1b/manim). My goal is to
create this completely on my own, though I've taken a few things from his
project (cited in source).

## Current State:

![Screenshot](Screenshot.png?raw=true "Screenshot")

## Requirements

To preview you only need to have the python requirements installed. You can
install them by running the following command:
```bash
> pip install --user -r requirements.txt
```

In order to save to a video, you will need FFmpeg

## Usage

```bash
> python main.py
```

### Command-line options

- No arguments: Defaults to `-p`
- `-f <filename>`: Export to the following file
  - Ex: `-f ./files/output/Test.mp4`
- `-h`: Enable high-quality rendering (1920 by 1080)
- `-m`: Enable medium-quality rendering (1280 by 720)
- `-p`: Preview the animation
- `-size<width>[x<height>]`: Manually set the render size
  - `-size<width>` will result in a 16 by 9 aspect ratio with the specified width
  - Ex: `-size1234x567` will set the render size to a width of 1234 and a height of 567
  - If no size is provided, it will default to 640 by 360

### Runtime options

- `p`: Pause/resume the animation
- `<enter>` or `<space>`: Step to the next frame when paused
- `<escape>`: Close the window

## Windows

To get this project setup on Windows, you'll need a few things:

- Python 3: [https://www.python.org/downloads/](https://www.python.org/downloads/)
  - You will also need to have the [VC++ 14.0 Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
    - Make sure to have the following selected:
      - C++ build tools 14.00

        ![Build Tools](files/images/BuildTools.png?raw=true "Build Tools")
      - Windows 10 SDK (any version should work, just remember which you used)

        ![Windows 10 SDK](files/images/Win10SDK.png?raw=true "Windows 10 SDK")
    - Once installed, add the Windows 10 SDK bin directory to the PATH
      - Path should be something like: C:\Program Files (x86)\Windows Kits\10\bin\\`<SDK Version>`\x64
    - You may also need to upgrade the `setuptools` package once this is installed
      ```bash
      > pip install --upgrade setuptools
      ```
- TeX Live: [https://www.tug.org/texlive/quickinstall.html](https://www.tug.org/texlive/quickinstall.html)
  - I chose the simple installation with all default settings (this will take a while)
- FFmpeg: [http://adaptivesamples.com/how-to-install-ffmpeg-on-windows/](http://adaptivesamples.com/how-to-install-ffmpeg-on-windows/)
  - I recommend using the latest stable build, rather than the nightly build
- dvisvgm: [https://dvisvgm.de/Downloads/](https://dvisvgm.de/Downloads/)
  - This will fix a memory issue that occurs with the version shipped with TeX Live
    - Note: I'm uncertain if this is still mandatory, if you don't run into any issues feel free to leave this off
  - Extract the zip to any folder you like, but make sure to put this before TeX Live in the PATH
