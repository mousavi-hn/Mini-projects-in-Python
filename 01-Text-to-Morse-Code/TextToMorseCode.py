class TextToMorseCode:
    def __init__(self, text):
        self.text = text.upper()

    def convert(self):
        morse_code = ""
        for c in self.text :
            morse_character = self.map_character_to_morse_code(c)
            if morse_character is not None:
                morse_code += morse_character
            else:
                morse_code += c
        return morse_code


    def map_character_to_morse_code(self, character):
        morse_code_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
            '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
            '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
            '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
        }

        return morse_code_dict.get(character)


