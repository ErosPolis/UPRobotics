import xbox
import robot

joy = xbox.Joystick()


if __name__ == "__main__":
    if(joy.A == 1):
        print("Clickeando")



