import pyautogui
import time
import threading

# The number of times you want to paste (you can change this)
paste_count = 100

# Delay between pasting operations (in seconds, you can change this)
delay_between_pastes = 0.5


# Function to perform the paste operation


def perform_paste():
    for _ in range(paste_count):
        # Simulate Ctrl+V (paste) keyboard shortcut
        pyautogui.hotkey('ctrl', 'v')

        # Simulate pressing the "Enter" key
        pyautogui.press('enter')

        # Wait for the specified delay before pasting again
        # time.sleep(delay_between_pastes)


# Create three threads to perform the paste operation
threads = []
for _ in range(13):
    thread = threading.Thread(target=perform_paste)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
