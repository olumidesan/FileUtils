## Create a screenshot by clicking the edges of the area you want to capture.

Note: Incomplete due to pynput `mouse.scroll()` issue*

## Requirements
  - Python 3.3+
  - [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/index.html)    ```pip install pyautogui```
  - [Pynput](https://pynput.readthedocs.io/en/latest/#)     ```pip install pynput```
  - Numpy
  
    On Linux, ```pyautogui``` has some extra dependencies. Simply run the following commands from the terminal to install them:
    ```sudo pip3 install python3-xlib```, 
    ```sudo apt-get install scrot```, 
    ```sudo apt-get install python3-tk```, and 
    ```sudo apt-get install python3-dev``` 
  
## How to Use
  1. After installing the required packages, simply run the script from the folder you want the screenshot to be saved.
  2. **Click** the edges of the area in the following order: top-left, top-right, bottom-left, bottom-right. (Note that it's not a bounding box--there's no dragging; but only _clicking_ of the edges of the intended image)
  
### Motivation
I needed to be able to take screenshots of a whole page, not just a snip of some area on the page. With this project I tried to create a script that automatically scrolled down the page (per my command), taking screenshots as it scrolled. It works currently, but not as I want it to.
