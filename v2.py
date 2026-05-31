import random
import time
import threading
from datetime import datetime, timedelta

import pyautogui
from pynput import mouse

# ---------------------------------------------------------------------------
# Keep-Alive: runs AUTOMATICALLY on start.
# Stops ONLY when you press Ctrl+C in the terminal.
# Double right-click (within 500 ms) also toggles pause/resume if needed.
# Fail-safe corner trigger is IGNORED -- it just recovers and keeps going.
# ---------------------------------------------------------------------------

# Disable PyAutoGUI's built-in fail-safe so a corner never crashes the script.
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05

moving_active = True          # START RUNNING IMMEDIATELY
right_click_times = []
delay_range = (6, 10)         # Seconds between actions

EDGE_MARGIN = 150             # Keep cursor this far from screen edges


def on_click(x, y, button, pressed):
    """Double right-click to manually pause/resume (optional)."""
    global moving_active, right_click_times

    if pressed and button == mouse.Button.right:
        right_click_times.append(datetime.now())
        right_click_times = right_click_times[-2:]

        if (
            len(right_click_times) == 2
            and right_click_times[-1] - right_click_times[0] <= timedelta(milliseconds=500)
        ):
            moving_active = not moving_active
            status = "PAUSED (double right-click again to resume)" if not moving_active else "RESUMED"
            print(f"[{_now()}] Keep-alive {status}.")
            right_click_times.clear()


def mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def _now():
    return datetime.now().strftime("%H:%M:%S")


def _clamp(value, low, high):
    return max(low, min(high, value))


def _safe_center():
    """Return a safe center-ish position if cursor is stuck near an edge."""
    width, height = pyautogui.size()
    return width // 2 + random.randint(-100, 100), height // 2 + random.randint(-100, 100)


def small_mouse_move():
    """Drift the cursor a short random distance. Recover if near a corner."""
    width, height = pyautogui.size()
    cur_x, cur_y = pyautogui.position()

    new_x = cur_x + random.randint(-250, 250)
    new_y = cur_y + random.randint(-250, 250)

    new_x = _clamp(new_x, EDGE_MARGIN, width - EDGE_MARGIN)
    new_y = _clamp(new_y, EDGE_MARGIN, height - EDGE_MARGIN)

    # If cursor is dangerously close to any corner, move to center first.
    near_corner = (
        (cur_x < EDGE_MARGIN or cur_x > width - EDGE_MARGIN) and
        (cur_y < EDGE_MARGIN or cur_y > height - EDGE_MARGIN)
    )
    if near_corner:
        safe_x, safe_y = _safe_center()
        pyautogui.moveTo(safe_x, safe_y, duration=0.5)
        print(f"[{_now()}] Cursor was near corner -- moved to center, continuing.")
        return

    pyautogui.moveTo(new_x, new_y, duration=random.uniform(0.4, 1.2))


def small_scroll():
    """Scroll a few wheel ticks up or down."""
    ticks = random.choice([-3, -2, -1, 1, 2, 3])
    pyautogui.scroll(ticks)


def keep_alive_action():
    """One random non-clicking action."""
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
    action_count = 0

    while True:
        if moving_active:
            try:
                keep_alive_action()
                action_count += 1
                sleep_time = random.uniform(*delay_range)
                print(f"[{_now()}] Action #{action_count} done. Next in {sleep_time:.1f}s.")
                time.sleep(sleep_time)

            except Exception as e:
                # Catch ANY error (including unexpected PyAutoGUI issues),
                # log it, and keep going -- never stop.
                print(f"[{_now()}] Warning: {e} -- recovering and continuing.")
                time.sleep(2)
        else:
            time.sleep(0.2)


def main():
    print("=" * 55)
    print("RUNNING AUTOMATICALLY")
    print("=" * 55)
    print("  * Stops ONLY when you press Ctrl+C here.")
    print("  * Double right-click to pause/resume anytime.")
    print("  * Corner fail-safe is DISABLED -- always recovers.")
    print("=" * 55)

    listener_thread = threading.Thread(target=mouse_listener, daemon=True)
    listener_thread.start()

    try:
        keep_alive_loop()
    except KeyboardInterrupt:
        print(f"\n[{_now()}] Stopped by Ctrl+C. Bye!")


if __name__ == "__main__":
    main()
