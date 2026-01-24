class MorseCodeToText:
    def __init__(self, code):
        self.code = code

    def decode(self):
        text = ""
        morse_chars = self.code.split()
        for c in morse_chars :
            character = self.map_morse_code_to_character(c)
            if character is not None:
                text += character
        return text


    def map_morse_code_to_character(self, character):
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

        reverse_dict = {v: k for k, v in morse_code_dict.items()}

        return reverse_dict.get(character)


