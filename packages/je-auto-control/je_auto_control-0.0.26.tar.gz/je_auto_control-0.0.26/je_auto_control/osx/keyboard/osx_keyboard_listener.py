import sys

import Quartz


def check_key_is_press(key_code):
    return Quartz.CGEventSourceKeyState(0, key_code)


if __name__ == "__main__":
    while True:
        temp = check_key_is_press(0x60)
        if temp:
            print(temp)
            sys.exit(0)
