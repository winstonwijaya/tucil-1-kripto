import numpy as np
import random
import re
import string

# matrix for full vigene cipher --> save to external file
# full_chip_matrix = np.empty((26,26))
MAX_MATRIX_SIZE = 26
DECRYPTION_ERROR = "Please encrypt first before proceeding to decryption process"
ALPHBET_CHOICE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def load_plain_text(filename):
    text = ""
    with open(filename) as files:
        text = files.read() 
    return text

def save_file(filename, text):
    with open(filename, 'w') as files:
        files.write(text)

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

def generate_full_vigenere_key():
    selected_keys = []
    key = ""
    while(len(key) < 26):
            random_char = random.choice(ALPHBET_CHOICE)
            if not random_char in key:
                key += random_char
    for item in key:
        selected_keys.append(list(item))
    
    options = list(ALPHBET_CHOICE)
    print(options)
    while(len(selected_keys[0])<26):
        selected_chars = ""
        for item in selected_keys:
            random_char = random.choice([x for x in options if x not in item and x not in selected_chars])
            print(options)
            print([x for x in options if x not in item and x not in selected_chars])
            # while (random_char in selected_chars) or (random_char in item):
            #     random_char = random.choice(ALPHBET_CHOICE)
            selected_chars += random_char
            item += random_char
            # print(item)

    # print(selected_keys)
    return selected_keys

def vigenere_standard(text, key, opt):
    temp_text = clear_text(text).upper()
    new_key = generate_key_repeat(text, key).upper()
    new_text = ""

    # opt = 0 --> encrypt, opt = 1 --> decrypt
    if(opt == 0):
        for char, key in zip(temp_text, new_key):
            new_text += chr(65 + (ord(char)+ord(key)) % 26)
    else:
        for char, key in zip(temp_text, new_key):
            new_text += chr(65 + (ord(char)-ord(key)) % 26)
        new_text = new_text.lower()
    return new_text

def split_text(text, length):
    lists = []
    start_pos = 0
    while start_pos != len(text):
        if(start_pos + length < len(text)):
            lists.append( text[ start_pos : (start_pos+ length)])
            start_pos += length
        else:
            lists.append(text[ start_pos : len(text)])
            start_pos = len(text)
    return lists      

def vigenere_full(text, key, opt):
    temp_text = clear_text(text).upper()
    new_key = generate_key_repeat(temp_text, key).upper()
    new_text = ""
    # print(temp_text)
    if(opt == 0):
        keys = generate_full_vigenere_key()
        temp = []
        for item in keys:
            temp_str = "".join(item)
            temp.append(temp_str)

        save_file('keystore.txt', temp_text + "," + ''.join(temp))
              
        for char, temp_key in zip(temp_text, new_key):
            print(ord(char)-65, ord(temp_key)-65)
            new_text += keys[ord(char)-65][ord(temp_key)-65]
        print(new_text)
    else:
        temp = load_plain_text('keystore.txt').split(",")
        keys = split_text(temp[1], 26)
        print(keys)
        for char, temp_key in zip(temp_text, new_key):
            idx = 0
            for id, val in enumerate(keys):
                if(char == val[ord(temp_key)-65]):
                    print(id,ord(temp_key)-65)
                    idx = id
                    break
            new_text += chr(idx+65)
        print(new_text.lower())
    

if __name__ == "__main__":
    # temp = load_plain_text("README.md")
    # print(temp)

    # print(vigenere_standard("LVVQHZNGFHRVL", "sonysonysonyss", 1))
    # print(generate_key_repeat("testtests", "test"))
    # print(generate_full_vigenere_key())
    vigenere_full("test", "temp", 0)