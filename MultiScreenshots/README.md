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
  1. The most relevant public method in the ```Screenshot``` class is ```take()```, which takes a screenshot.
  Simply call it directly and pass in your desired options. E.g:
  
    ```Screenshot().take(multiple=True, merged=True)``` -> Take multiple screenshots and finally merge them into one file.
    
    ```Screenshot().take(multiple=True)``` -> Take multiple screenshots and don't merge them.
    
    ```Screenshot().take()``` -> Take a single screenshot.

  2. After installing the required packages, simply run the script from the folder you want the screenshot to be saved i.e. ```python3 ms.py```. The console then prompts for mouse clicks as below.
  3. **Click** the edges of the area in the following order: top-left, top-right, bottom-left, bottom-right. (Note that it's not a bounding box--there's no dragging, but only **clicking** of the edges of the intended image).
  4. After taking the first screenshot, if the ```multiple``` flag of the ```Screenshot``` class was set to ```True```, you'll be prompted with one of three keyboard options which does the corresponding action on the right.
  ```Shift``` ==> ```Manualy take another screenshot```
  ```Ctrl``` ==> ```Automatically continue taking screenshots```
  ```Esc``` ==> ```Stop taking screenshots now```
  5. If ```Ctrl``` is pressed, i.e screenshots should be taken automatically, to stop this once done, ```Ctrl``` should be pressed again.
  
  You can also watch [the included video](example.mp4)
  
### Motivation
I needed to screenshoot a whole page on Chrome, and did not want to have to take a screenshot, scroll down, take another screenshot, etc. I wanted everything on the page as one picture, with a command called once. With this project I tried to create a script that automatically scrolled down the page (per my command), taking screenshots as it scrolled and merging them into one picture (if required). 

### Known Issues
1. It works on Chrome but doesn't on some other applications, due to some issues with Pyautogui's ```scroll()``` method.
2. The scrolling is noticeably slow. This was actually delibrate, as an alternative to the ```scroll()``` method issues from both Pyautogui and Pynput.
3. The merging of images into one isn't perfect yet. There are edge cases.

Contributions/Corrections are more than welcome!


