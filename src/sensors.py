import re


class Translator:

    # Divides the chain every two digits
    @staticmethod
    def divide(chain=""):
        hexadecimal = re.findall('..', chain)
        return hexadecimal

    # Converts bytes to readable data
    @staticmethod
    def co2_translate(chain=""):
        hexadecimal = re.findall('..', chain)
        for i in range(0, len(hexadecimal)):
            hexadecimal[i] = str(int(hexadecimal[i], 16))
        hexadecimal[3] = str((int(hexadecimal[3]) // 254) + 1) + "." + str((int(hexadecimal[4]) % 254) + 1)
        hexadecimal.pop(4)
        return hex
