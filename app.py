import random
import time
import threading
from pynput import mouse
import pyautogui
from datetime import datetime, timedelta

# Global variables
moving_active = False  # Flag to indicate if mouse movement is active
right_click_times = []  # To track double right-clicks
delay_range = (6, 10)  # Default delay range (in seconds)

# Mouse controller instance
mouse_controller = mouse.Controller()

def on_click(x, y, button, pressed):
    global moving_active, right_click_times
    
    if pressed and button == mouse.Button.right:
        # Record the time of the right-click
        right_click_times.append(datetime.now())
        
        # Keep only the last 2 right-click times
        right_click_times = right_click_times[-2:]
        
        # Check for double right-click within 500 ms
        if len(right_click_times) == 2 and (right_click_times[-1] - right_click_times[0] <= timedelta(milliseconds=500)):
            # Toggle the mouse movement
            moving_active = not moving_active
            if moving_active:
                print("Mouse movement started.")
            else:
                print("Mouse movement stopped.")
            right_click_times.clear()  # Clear click times to avoid multiple detections

def mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def random_mouse_move():
    global moving_active, delay_range
    
    while True:
        if moving_active:
            # Get random screen coordinates
            width, height = pyautogui.size()
            random_x = random.randint(0, width)
            random_y = random.randint(0, height)
            
            # Move the mouse smoothly to the random position
            pyautogui.moveTo(random_x, random_y, duration=random.uniform(0.5, 1.5))  # Move with random speed
            
            # Wait for a random delay before the next move
            delay = random.uniform(*delay_range)
            time.sleep(delay)
        else:
            time.sleep(0.1)  # Check every 0.1 seconds if movement is activated

def main():
    # Start the mouse listener in a separate thread
    mouse_thread = threading.Thread(target=mouse_listener)
    mouse_thread.start()

    # Start the random mouse movement in the main thread
    random_mouse_move()

if __name__ == "__main__":
    main()
