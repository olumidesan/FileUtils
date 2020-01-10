
import os
import PIL
import time
import atexit
import numpy as np
import pyautogui as gui

from math import ceil
from pynput import keyboard
from contextlib import suppress
from multiprocessing import Process, Manager
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Controller as MouseController


mouse = MouseController() # Create a mouse controller object

# Save resulting images to the location of this script
SAVE_DIR = os.path.abspath(os.path.dirname(__file__))

# Key commands
SHIFT_KEYS = {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r} # Any of the `Shift` keys
CTRL_KEYS = {keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l} # Any of the `Ctrl` keys
ESC_KEY = keyboard.Key.esc # `Esc` key


def controlled_scroll(length):
    """Finer control of scroll behaviour"""

    for _ in range(length):
        gui.scroll(-1)

    # mouse.scroll(0, -length)


class Screenshot:
    """
    Class for creating single/multiple/merged screenshots.

    :param :multiple -> bool: Flag that determines if multiple screenshots are being taken
    :param :merge -> bool: Flag that determines if the multiple screenshots should be merged
                           into one.
    """
 
    # Used for pixel subtraction and may differ per one's system resolution.
    # This value was gotten by tests and intrapolation for a Windows system 
    # with resolution of 1366x768. How? -> A 136 pixel difference mapped to 70 scrolls.
    # Will later create a `calibrate` function

    # Essentially, the `mouse` is meant to scroll down the vertical height of the 
    # first screenshot, and how much this is should ideally be the difference between
    # the `y` coordinate of the top-right and bottom-right of the first screenshot, but
    # for some reason pynput's mouse.scroll() method behaves erratically. And so does 
    # pyautogui's `scroll()` method.

    # Some applications also have different scroll behaviour and this may affect the scroll
    # behaviour, not to mention webpages with specific CSS. This factor works with an accuracy
    # of 97% on Chrome, which is what instigated the project in the first place, so I'm [currently] 
    # okay with it.
    PIXEL_FACTOR = (70/136) # /2.05) 
    
    def __init__(self, multiple:bool=False, merge:bool=False):
        self.is_multiple = multiple
        self.should_be_merged = merge 

        self._counter = 0 # Counter for mapping mouse clicks to positions
        self._shot_region = () # Tuple containing the x,y coordinates of a clicked region

        # `Manager.dict()` needed for inter-process communication
        self._mgr = Manager().dict()
        self._mgr['now'] = time.time() # Save a copy of the current time
        self._mgr['shots_count'] = 0 # Counter for the number of screenshots made 
        self._mgr['auto_mode'] = False # A mode flag

        # Screen Coordinates
        self._coordinates = {'top_left': [], 'top_right': [],
                             'bottom_left': [], 'bottom_right': []}        

    def _track_keyboard_presses(self, key):
        """
        Starts Keyboard event listener that continues/stops the screenshooting process
        based on the pressed key
        """
        if key in SHIFT_KEYS: # Continue manual screenshooting
            self._screenshoot()
        
        elif key in CTRL_KEYS: # Continue automatic screenshooting  
            self._mgr['auto_mode'] = True # Set the flag globally
            return False
        
        elif key == ESC_KEY: # Stop screenshooting immediately
            return False # Kill the listener

    def _track_mouse_clicks(self, x, y, button, pressed):
        if pressed:
            self._counter += 1
            if self._counter % 4 == 1:
                self._coordinates['top_left'] = (x, y)
                return False  # stop the listener

            elif self._counter % 4 == 2:
                self._coordinates['top_right'] = (x, y)
                return False

            elif self._counter % 4 == 3:
                self._coordinates['bottom_left'] = (x, y)
                return False

            elif self._counter % 4 == 0:
                self._coordinates['bottom_right'] = (x, y)
                return False


    def _start_mouse_listener(self):
        """Creates the listener object that tracks mouse clicks"""

        with MouseListener(on_click=self._track_mouse_clicks) as ml:
            ml.join()   

    def _start_keyboard_listener(self):
        """Creates the listener object that tracks keyboard presses"""

        print(f"\n {'Screenshot Keyboard Options':^10}: \
                \n `Shift` {'==>':^5} Manualy take another screenshot. \
                \n `Ctrl` {'==>':^5} Automatically continue taking screenshots (Press `Ctrl+C` to end). \
                \n `Esc` {'==>':^5} Stop taking screenshots now.\n")
        with keyboard.Listener(on_press=self._track_keyboard_presses) as kl:
            kl.join() 

    def _set_shot_region(self):
        """Formats the coordinates for use with PyAutoGui"""

        width = max(self._coordinates['top_right'][0] - self._coordinates['top_left'][0],
                    self._coordinates['bottom_right'][0] - self._coordinates['bottom_left'][0])
        height = max(self._coordinates['bottom_right'][1] - self._coordinates['top_right']
                    [1], self._coordinates['bottom_left'][1] - self._coordinates['top_left'][1])
        
        left = self._coordinates['top_left'][0]
        top = self._coordinates['top_left'][1]

        self._shot_region = (left, top, width, height)
    
    @staticmethod
    def merge_screenshots(shots:list):
        """Merges a list of image files (screenshots) into one"""

        imgs = []

        # Create an array of all the individual screenshots
        for i in shots:
            with suppress(FileNotFoundError):
                imgs.append(PIL.Image.open(i))        

        # Vertically stack them
        try:
            min_shape = sorted([(np.sum(i.size), i.size ) for i in imgs])[-1][1]
            imgs_comb = np.vstack([np.asarray(i.resize(min_shape)) for i in imgs])
            imgs_comb = PIL.Image.fromarray(imgs_comb)
        
        # Raise the appropriate exception        
        except Exception: 
            raise

        # Save the resulting image
        imgs_comb.save(f"merged_screenshot_{time.strftime('%H%M%S')}.png")
    
    def _position_mouse(self):
        """
        Positions the mouse at its required position for correct screenshooting.
        Just in case the mouse position has changed before the next screenshot.
        """
        # Use the top-right as the screenshot anchor i.e set the mouse there.    
        mouse.position = self._coordinates.get('top_right') 

    def _screenshoot(self):
        """Captures an image of the `shot_region` area"""
        
        # Scroll the vertical height of the window to take the next screenshot
        scroll_length = ceil(self.PIXEL_FACTOR * self._shot_region[-1]) + 2
        
        self._position_mouse()
        controlled_scroll(scroll_length)

        time.sleep(0.5) # Ensure scrolling has stopped
        gui.screenshot(region=self._shot_region).save(f"temp_{self._mgr['now']}_{self._mgr['shots_count']}.png")
        
        # Increase the number of screenshots taken
        self._mgr['shots_count'] += 1 
    
    def _cleanup(self):
        """Removes the temporarily created image file(s)"""

        for i in range(self._mgr['shots_count'] + 1):
            fn = f"temp_{self._mgr['now']}_{i}.png"
            with suppress(OSError):
                os.remove(fn)        
                                 
    def take(self):
        """Starts screenshooting"""

        positions = [' '.join(i.split('_')) for i in self._coordinates.keys()]

        for i in positions:
            print(f"Click the {i} of the screenshot")
            self._start_mouse_listener()  # Start the mouse listener

        self._set_shot_region()
        
        # Create a screenshot using the clicked coordinates.
        # The coordinates set the anchor for the size of the
        # consequent screenshots.
        gui.screenshot(region=self._shot_region).save(f"temp_{self._mgr['now']}_{self._mgr['shots_count']}.png")  
        end_message = f"Screenshot taken. Image file saved to {SAVE_DIR}."   

        if self.is_multiple:
            self._mgr['shots_count'] += 1          
            end_message = "Finished taking screenshots.\n"

            # Get ready
            time.sleep(0.5)
            self._position_mouse()

            # Start the keyboard listener in a separate process.
            # This prevents GIL clash between the mouse and the keyboard listeners.
            klp = Process(target=self._start_keyboard_listener)
            klp.start()
            klp.join()

            # Automatic screenshot mode
            if self._mgr['auto_mode']:
                print("\nIn auto-screenshot mode. Press `Ctrl+C` to stop.")
                while 1:
                    try:
                        self._screenshoot()
                    # `Ctrl + C` stops the continuous scroll
                    except KeyboardInterrupt:
                        break

            if self.should_be_merged:
                shots = [f"temp_{self._mgr['now']}_{j}.png" for j in range(self._mgr['shots_count'])]            
                Screenshot.merge_screenshots(shots)   

                # Cleanup individual image files upon exit since 
                # they've been merged
                atexit.register(self._cleanup)
                end_message += f"Combined image file saved to {SAVE_DIR}."
            else:
                end_message += f"Files saved to {SAVE_DIR}."                

        print(end_message)

# Screenshot(multiple=True, merge=False).take() if __name__ == "__main__" else None

