import random
import time
import threading
from datetime import datetime, timedelta

import pyautogui
from pynput import mouse

# ---------------------------------------------------------------------------
# Keep-Alive: prevents Google Colab (or any other tool that idles out) from
# sleeping by simulating gentle user activity. The script ONLY moves the mouse
# a little or scrolls the wheel a few ticks -- it never clicks anything, so it
# will not interact with whatever window is focused.
#
# Toggle the activity on/off with a quick double right-click (within 500 ms).
# ---------------------------------------------------------------------------

# Global state
moving_active = False        # Is the keep-alive activity currently running?
right_click_times = []       # Used to detect a double right-click toggle
delay_range = (6, 10)        # Seconds between actions (random in this range)

# Keep the cursor at least this many pixels away from any screen edge so we
# never trigger PyAutoGUI's corner fail-safe.
EDGE_MARGIN = 100

# Small pause between PyAutoGUI calls (default is 0.1s).
pyautogui.PAUSE = 0.05


def on_click(x, y, button, pressed):
    """Detect a double right-click and toggle the keep-alive activity."""
    global moving_active, right_click_times

    if pressed and button == mouse.Button.right:
        right_click_times.append(datetime.now())
        right_click_times = right_click_times[-2:]

        if (
            len(right_click_times) == 2
            and right_click_times[-1] - right_click_times[0] <= timedelta(milliseconds=500)
        ):
            moving_active = not moving_active
            print("Keep-alive started." if moving_active else "Keep-alive stopped.")
            right_click_times.clear()


def mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def _clamp(value, low, high):
    return max(low, min(high, value))


def small_mouse_move():
    """Drift the cursor a short distance from where it currently is."""
    width, height = pyautogui.size()
    cur_x, cur_y = pyautogui.position()

    # Small offset, so it feels like a person nudging the mouse.
    new_x = cur_x + random.randint(-250, 250)
    new_y = cur_y + random.randint(-250, 250)

    # Stay well inside the screen, away from the corners.
    new_x = _clamp(new_x, EDGE_MARGIN, width - EDGE_MARGIN)
    new_y = _clamp(new_y, EDGE_MARGIN, height - EDGE_MARGIN)

    pyautogui.moveTo(new_x, new_y, duration=random.uniform(0.4, 1.2))


def small_scroll():
    """Scroll a few wheel ticks up or down. No clicks."""
    ticks = random.choice([-3, -2, -1, 1, 2, 3])
    pyautogui.scroll(ticks)


def keep_alive_action():
    """Perform one random non-clicking action: a small move or a small scroll."""
    # Bias slightly toward mouse movement, since some apps register that more
    # readily than scroll events.
    action = random.choices(
        population=("move", "scroll"),
        weights=(0.7, 0.3),
        k=1,
    )[0]

    if action == "move":
        small_mouse_move()
    else:
        small_scroll()


def keep_alive_loop():
    global moving_active

    while True:
        if moving_active:
            try:
                keep_alive_action()
            except pyautogui.FailSafeException:
                # The cursor hit a screen corner (likely the user grabbing back
                # control). Pause instead of crashing.
                print(
                    "Fail-safe triggered (mouse reached a screen corner). "
                    "Keep-alive paused. Double right-click to resume."
                )
                moving_active = False
                continue

            time.sleep(random.uniform(*delay_range))
        else:
            time.sleep(0.1)


def main():
    print(
        "Keep-Alive ready.\n"
        "  - Double right-click (within 500 ms) to start/stop.\n"
        "  - Move the mouse to a screen corner to emergency-stop.\n"
        "  - Tip: leave your cursor hovering over the Colab tab so the\n"
        "    activity is registered by the browser."
    )

    listener_thread = threading.Thread(target=mouse_listener, daemon=True)
    listener_thread.start()

    keep_alive_loop()


if __name__ == "__main__":
    main()
