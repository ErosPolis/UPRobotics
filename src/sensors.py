import re
import robot

class CO2_Translate:

    @staticmethod
    def divide(chain=""):
    	#Divides the chain every two digits
        hexa = re.findall('..',chain) 
        return hexa

    @staticmethod
    def CO2Convert(chain=""):
    	#Divides the chain every two digits
        hexa = re.findall('..', chain)
        #Converts the values from hexadecimal to decimal  
        for i in range(0, len(hexa)):
            hexa[i] = str(int(hexa[i],16))
        # Byte 4 y 5 combined in one 
        hexa[3] = str((int(hexa[3])//254) + 1) + "." + str((int(hexa[4])%254) + 1)
        hexa.pop(4)
        return hexa
