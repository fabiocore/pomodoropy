#!/usr/bin/env python

import sys
import time
import platform
from plyer import notification
import shutil
from tqdm import tqdm

if platform.system() == "Darwin":
    import pync

with open("stdout_redirected.txt", "w") as f:
    sys.stdout = f
    import pygame
sys.stdout = sys.__stdout__


def send_notification(title, message):
    if platform.system() == "Darwin":
        pync.notify(message, title=title)
    else:
        notification.notify(
            title=title,
            message=message,
            app_icon=None,
            timeout=10,
        )


def play_level_up_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)


def progress_bar(duration, interval):
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    purple_bar_format = "{l_bar}%s{bar}%s{r_bar}" % ("\033[1;35m", "\033[0m")
    try:
        for _ in tqdm(
            range(int(duration * 60 / interval)),
            ncols=terminal_width,
            bar_format=purple_bar_format,
        ):
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nAborting timer...")
        sys.exit(0)


def pomodoro_timer(minutes):
    print(f"Starting {minutes}-minute timer...")
    print("Press Ctrl+C to abort.")
    progress_bar(minutes, 1)
    play_level_up_sound()
    send_notification("Pomodoro Timer", f"{minutes}-minute timer is up!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: tomato.py [focus|short-break|long-break|custom_minutes]")
        sys.exit(1)

    timers = {
        "focus": 25,
        "short-break": 7.5,
        "long-break": 15,
    }

    option = sys.argv[1]

    if option in timers:
        pomodoro_timer(timers[option])
    elif option.isdigit():
        pomodoro_timer(int(option))
    else:
        print(
            "Invalid option. Usage: tomato.py [focus|short-break|long-break|custom_minutes]"
        )
        sys.exit(1)
