import xboxcontroller
import time
import robot

joy = xboxcontroller.Joystick()

def test_buttons():
    print("-----------------------------------------------------------")
    print(joy.a())


if __name__ == "__main__":
    while True:
        print(joy.a())
        time.sleep()






