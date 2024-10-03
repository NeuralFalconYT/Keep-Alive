
# Auto Mouse Mover for Activity Keep-Alive

This script moves the mouse randomly at intervals to simulate user activity and prevent apps or systems from going idle. You can start or stop the mouse movement with a double right-click.

## Features
- **Random mouse movement** to keep apps active.
- **Double right-click** to start and stop the mouse movement.
- **Configurable delay** between movements.

## Requirements

Before running the script, make sure you have Python installed. You can install the required packages using `pip`.

### Installation

1. Clone this repository or download the script files.
2. Install the dependencies by running:

    ```bash
    pip install -r requirements.txt
    ```

### Dependencies

- `pynput` - for capturing mouse input.
- `pyautogui` - for controlling the mouse movements.

### Running the Script

To run the auto mouse mover:

```bash
python app.py
```

Once the script is running:

1. **Activate**: Double right-click anywhere on the screen to start the mouse movement.
2. **Deactivate**: Double right-click again to stop the movement.

### Customizing the Delay

You can modify the delay between mouse movements by changing the `delay_range` in the script:

```python
delay_range = (6, 10)  # Change this to any range you want, e.g.,(1,6), (2, 8),(min,max)
```

This specifies the minimum and maximum time (in seconds) between each random mouse movement.

### Notes

- The script works by moving the mouse to random positions on the screen with a smooth transition to simulate normal user activity.
- You can stop the script anytime by pressing `CTRL + C` in the terminal.

### Example Use Cases

- Prevent apps from going idle.
- Keep online sessions active.
- Avoid auto-logouts from inactivity.

### License

This project is open source and available under the MIT License.
```

### Instructions Summary:
- **Install** dependencies with `pip install -r requirements.txt`.
- **Start/stop** mouse movement with a double right-click.
- **Change the delay** between movements by modifying `delay_range` in the script.
