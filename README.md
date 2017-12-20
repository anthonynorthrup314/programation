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

To preview you only need to have the python2 requirements installed. You can
install them by running the following command:
```bash
> pip2 install --user -r requirements.txt
```

In order to save to a video, you will need FFmpeg

## Windows

To get this project setup on Windows, you'll need a few things:

- Git: [https://gitforwindows.org/](https://gitforwindows.org/)
  - This also installs Git Bash, which is helpful
- Python 2.7: [https://www.python.org/downloads/](https://www.python.org/downloads/)
  - Make sure this comes with pip, if not, follow [these instructions](https://stackoverflow.com/a/12476379/8945895)
  - I added the following to my `.bashrc`
    
    ```bash
    alias python2="/c/Python27/python.exe"
    alias pythonw2="/c/Python27/pythonw.exe"
    ```
    
  - You will also need to have the [Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)
- TeX Live: [https://www.tug.org/texlive/quickinstall.html](https://www.tug.org/texlive/quickinstall.html)
  - I chose the simple installation with all default settings (this will take a while)
- FFmpeg: [http://adaptivesamples.com/how-to-install-ffmpeg-on-windows/](http://adaptivesamples.com/how-to-install-ffmpeg-on-windows/)
  - I recommend using the latest stable build, rather than the nightly build
- dvisvgm: [http://dvisvgm.bplaced.net/Downloads](http://dvisvgm.bplaced.net/Downloads)
  - This will fix a memory issue that occurs with the version shipped with TeX Live
  - Extract the zip to any folder you like, but make sure to put this before TeX Live in the PATH
