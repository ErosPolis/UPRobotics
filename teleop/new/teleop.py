import xboxcontroller
import robot

joy = xboxcontroller.Joystick()
robot = robot.Robot()

if __name__ == "__main__":
    while True:
        left_stick_x, left_stick_y = robot.st(joy.left_x(), joy.right_x())