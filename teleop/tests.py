import xbox
import robot

joy = xbox.Joystick()


if __name__ == "__main__":
    m1, m2 = robot.st(joy.leftX(), joy.leftY())


