from TextToMorseCode import TextToMorseCode

plainText = input("Please insert the text: ")
morseCode = TextToMorseCode(plainText)
print(morseCode.convert())