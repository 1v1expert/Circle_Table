# The rotary table control program
![Screenshot](https://github.com/1v1expert/Circle_Table/raw/develop/img/TmpSVG1.jpg)

### 3DCircle program

![3DCircle program](https://github.com/1v1expert/Circle_Table/raw/master/img/screenshot.png)

## Installation:
The generic steps that should basically be done regardless of operating system
and runtime environment are the following (as *regular
user*, please keep your hands *off* of the `sudo` command here!) - this assumes
you already have Python 3, pip and virtualenv set up on your system:

1. Checkout 3DCircle: `git clone https://github.com/1v1expert/Circle_Table.git`
2. Change into the OctoPrint folder: `cd Circle_Table`
3. Create a user-owned virtual environment therein: `virtualenv venv`
4. Install OctoPrint *into that virtual environment*: `./venv/bin/pip install -r requirements.txt`l .
```
Dependencies:
- PyQT5
- Pyserial
```
## Configuration

If not specified via the command line, the config file `config.json` for OctoPrint is expected in the settings folder,
which is located at project.