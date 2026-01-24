from TextToMorseCode import TextToMorseCode
from MorseCodeToText import MorseCodeToText

choice = input("Please insert A or B:\nA. Text to Morse Code\nB. Morse Code To Text\n").upper()
if choice == "A":
    morseCode = TextToMorseCode(input("Please insert the text: "))
    print(morseCode.encode())
else:
    text = MorseCodeToText(input("Please insert the morse code: "))
    print(text.decode())