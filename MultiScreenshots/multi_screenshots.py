
import os
import PIL
import time
import atexit
import numpy as np
import pyautogui as gui

from pynput import keyboard
from contextlib import suppress
from pynput.mouse import Listener as MouseListener, Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener


SAVE_DIR = os.path.abspath(os.path.dirname(__file__))

SHIFT_KEYS = {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r} # Any of the `Shift` keys
CTRL_KEYS = {keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.ctrl_l} # Any of the `Ctrl` keys
ESC_KEY = keyboard.Key.esc


class Screenshot:
    """
    Class for creating single/multiple screenshots.
    Has one main public method (`make`) that invokes the screenshot(s)-making process.
    The rest are [pseudo] private.
    """
 
    # Used for pixel subtraction and may differ per your system resolution.
    # This value was gotten by tests and intrapolation for a Windows system 
    # with resolution of 1366x768 and converges to a 99% pixel closeness.
    PIXEL_FACTOR = -1#2.380
    
    def __init__(self):
        self._mouse = MouseController()
        self._counter = 0 # Counter for mapping mouse clicks to positions
        self._shots_count = 1 # Counter for the number of screenshots made
        self._now = time.time() # Save a copy of the current time
        self._shot_region = () # Tuple containing the x,y coordinates of a clicked region

        # Screen Coordinates
        self._coordinates = {'top_left': [], 'top_right': [],
                             'bottom_left': [], 'bottom_right': []}        

    def _track_keyboard_presses(self, key):
        """
        Starts Keyboard event listener that continues/stops the screenshooting process
        based on the pressed key
        """
        if key == ESC_KEY: return False # Kill the listener

        if key in SHIFT_KEYS: # Continue screenshooting
            self._screenshoot()

            # Delay for a bit to allow GIL activate the mouse thread
            time.sleep(2) 

        elif key in CTRL_KEYS: # Stop screenshooting
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

        print("\nPress `Shift` to continue screenshooting, or `Ctrl` to stop.\n")
        with keyboard.Listener(on_press=self._track_keyboard_presses) as kl:
            kl.join() 

    def _format_image(self):
        """Formats the coordinates for use with PyAutoGui"""

        width = max(self._coordinates['top_right'][0] - self._coordinates['top_left'][0],
                    self._coordinates['bottom_right'][0] - self._coordinates['bottom_left'][0])
        height = max(self._coordinates['bottom_right'][1] - self._coordinates['top_right']
                    [1], self._coordinates['bottom_left'][1] - self._coordinates['top_left'][1])
        
        left = self._coordinates['top_left'][0]
        top = self._coordinates['top_left'][1]

        self._shot_region = (left, top, width, height)
    
    def _create_image(self):
        """Creates the actual screenshot"""

        imgs = []
        shots = [f"temp_{self._now}_0.png"] + [f"temp_{self._now}_{j+1}.png" for j in range(self._shots_count)]

        # Create an array of all the individual screenshots
        for i in shots:
            with suppress(FileNotFoundError):
                imgs.append(PIL.Image.open(i))        

        # Vertically stack them
        try:
            min_shape = sorted([(np.sum(i.size), i.size ) for i in imgs])[-1][1]
            imgs_comb = np.vstack([np.asarray(i.resize(min_shape)) for i in imgs])
            imgs_comb = PIL.Image.fromarray(imgs_comb)
        except IndexError: # Only one screenshot was taken
            return

        # Save the resulting image
        imgs_comb.save(f"multishot_{time.strftime('%H%M%S')}.png")
    
    def _screenshoot(self):
        """Captures an image of the `shot_region` area"""

        # Simulate a delay so the GIL focuses on this [mouse] thread
        time.sleep(0.5)
        
        # Scroll the vertical height of the window to make the next screenshot
        self._mouse.scroll(0, self.PIXEL_FACTOR * self._shot_region[-1])
        time.sleep(1) # Ensure scrolling has stopped
        gui.screenshot(region=self._shot_region).save(f'temp_{self._now}_{self._shots_count}.png')
        
        # Increase the number of screenshots taken
        self._shots_count += 1 
    
    def _cleanup(self):
        """Removes the temporarily created image file(s)"""

        # If only one screenshot was taken, leave it
        if self._shots_count > 1:
            for i in range(self._shots_count + 1):
                fn = f'temp_{self._now}_{i}.png'
                with suppress(OSError):
                    os.remove(fn)        
                                 
    def make(self):
        """Starts screenshooting"""

        positions = [' '.join(i.split('_')) for i in self._coordinates.keys()]

        for i in positions:
            print(f"Click the {i} of the screenshot")
            self._start_mouse_listener()  # Start the mouse listener

        self._format_image()
        
        # Create a screenshot using the clicked coordinates.
        # The coordinates set the anchor for the size of the
        # consequent screenshots.
        gui.screenshot(region=self._shot_region).save(f'temp_{self._now}_0.png')            
        
        # Get ready
        time.sleep(0.5)
        # Use the top-right as the screenshot anchor. Set the mouse there.    
        self._mouse.position = self._coordinates.get('top_right') 

        self._start_keyboard_listener()
        self._create_image()
        
        print(f"Finished taking screenshots. \nCombined image file saved to {SAVE_DIR}.")

        # Cleanup temp files upon exit
        atexit.register(self._cleanup)


Screenshot().make() if __name__ == "__main__" else None

