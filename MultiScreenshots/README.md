## Create Multiple [Mergeable] Screenshots at once.

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
  2. **Click** the edges of the area in the following order: top-left, top-right, bottom-left, bottom-right. (Note that it's not a bounding box--there's no dragging; but only **clicking** of the edges of the intended image).
  3. There is really only one public method in the ```Screenshot``` class - ```take()```, so there's really no need to make an instance.
  Simply call it directly and pass in your desired options. E.g:
  
  ```Screenshot().take(multiple=True, merged=True)``` -> Take multiple screenshots and finally merge them into one file.
  
  ```Screenshot().take(multiple=True)``` -> Take multiple screenshots and don't merge them.
  
  ```Screenshot().take()``` -> Take a single screenshot.

  You can also watch ![](usage.mp4)
  
### Motivation
I needed to screenshoot a whole page on Chrome, and did not want to have to take a screenshot, scroll down, take another screenshot, etc. I wanted everything on the page as one picture, with a command called once. With this project I tried to create a script that automatically scrolled down the page (per my command), taking screenshots as it scrolled and merging them into one picture (if required). 

### Known Issues
1. It works on Chrome but doesn't on some other applications, due to some issues with Pyautogui's ```scroll()``` method.
2. The scrolling is notably slow. This was actually delibrate, as an alternative to the ```scroll()``` method issues from Pyautogui and Pynput.
3. The merging of images into one isn't perfect yet. There are edge cases.

Contributions are more than welcome!


