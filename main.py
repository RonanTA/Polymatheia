import pyautogui
import time
import random

def move_mouse(x, y):
    pyautogui.moveTo(x, y)

def click_mouse(button='left'):
    pyautogui.click(button=button)

def press_key(key):
    pyautogui.press(key)

def type_text(text):
    pyautogui.typewrite(text)



# Example Usage
if __name__ == "__main__":
    # Move mouse to coordinates (x, y)
    #move_mouse(1000, 1000)
    #time.sleep(1)

    # Move the mouse to the pixel whose coordinates you want to get
    pyautogui.moveTo(x=990, y=468)
    x=random.randint(0, 1000)
    y=random.randint(0, 1000)
    timeout=0
    while timeout<300 :
        pyautogui.moveTo(x,y)
        x+=random.randint(-10, 10)
        y+=random.randint(-10, 10)
        time.sleep(0.01)
        timeout+=1
        

    # Get the current mouse coordinates
    x, y = pyautogui.position()

    print(f"The pixel coordinates are: x={x}, y={y}")

    # Click the left mouse button
    #click_mouse('left')
    #time.sleep(1)

    # Press the 'a' key
    #press_key('a')
    #time.sleep(1)

    # Type the text "Hello, World!"
    #type_text('Hello, World!')
