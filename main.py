import re
import numpy as np

# matrix for full vigene cipher --> save to external file
full_chip_matrix = np.empty((26,26))

def load_plain_text(filename):
    files = open(filename, "r")
    text = files.read()
    files.close()

    return text

# clear non alphbet characters for standard vigenere and playfair cipher
def clear_text(text):
    pattern = re.compile('[^a-zA-Z]')
    return pattern.sub('', text)

#generate key for encryption and decryption by repeating input key
def generate_key_repeat(text, key):
    new_key = ''
    if len(text) >= len(key):
        res = len(key) - len(text) % len(key)
        diff = (len(text) // len(key)) + (1 if res != 0 else 0)
        new_key = key*diff
        new_key = new_key[:(len(new_key)-res)]
    else:
        new_key = key[: len(text)]
    return new_key


def vigenere_standard(text, key, opt):
    temp_text = clear_text(text).upper()
    new_key = generate_key_repeat(text, key).upper()
    new_text = ""

    if(opt == 0):
        for char, key in zip(temp_text, new_key):
            new_text += chr(65 + (ord(char)+ord(key)) % 26)
    else:
        for char, key in zip(temp_text, new_key):
            new_text += chr(65 + (ord(char)-ord(key)) % 26)
        new_text = new_text.lower()
    return new_text

if __name__ == "__main__":
    # temp = load_plain_text("README.md")
    # print(temp

    print(vigenere_standard("LVVQHZNGFHRVL", "sonysonysonyss", 1))
    # print(generate_key_repeat("testtests", "test"))
    