# import numpy as np
# import PIL
import time
# list_im = ['Test1.jpg', 'Test2.jpg', 'Test3.jpg']
# imgs    = [ PIL.Image.open(i) for i in list_im ]
# # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
# min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
# imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

# # save that beautiful picture
# imgs_comb = PIL.Image.fromarray( imgs_comb)
# imgs_comb.save( 'Trifecta.jpg' )    

# # for a vertical stacking it is simple: use vstack
# imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
# imgs_comb = PIL.Image.fromarray( imgs_comb)
# imgs_comb.save( 'Trifecta_vertical.jpg' )

from pynput.mouse import Button, Controller
import pyautogui as gui
mouse = Controller()

# Read pointer position
# print('The current pointer position is {0}'.format(
#     mouse.position))
# now = mouse.position

# while 1:
#     #if mouse.position[-1] - now[-1] == 405:
#     print(mouse.position)
#         #break
#     time.sleep(2)
# # Set pointer position
# mouse.position = (10, 20)
# print('Now we have moved it to {0}'.format(
#     mouse.position))

# # Move pointer relative to current position
# mouse.move(5, -5)

# # Press and release
# mouse.press(Button.left)
# mouse.release(Button.left)


# # Double click; this is different from pressing and releasing
# # twice on Mac OSX
# mouse.click(Button.left, 2)

# Scroll two steps down
print("Started")
time.sleep(2)
# gui.moveTo(967,307)

for i in range(83):
    # diff = gui.position()[-1] - 307
    # print(f"Current position is: {gui.position()}, and diff is {diff}")    
    # if diff in [134, 135, 136, 137, 138]:
    #     break
    gui.scroll(-3)
    print(i)

    #count+=1
    # time.sleep(0.2)
#print(gui.position())
print("Count is", "205")



# def scroller(l):
#     for _ in range(l):
#         gui.scroll(-1)
#         #time.sleep(0.000002)
    
#     return

# scroller(69)
# gui.scroll(-136)

# time.sleep(2);print(gui.position)
# mouse.position = (967, 307)
#print(mouse.position)
# time.sleep(1)
# mouse.scroll(0, -1*136)
# time.sleep(2)
# mouse.position
# print(mouse.position)