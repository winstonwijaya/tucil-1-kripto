import numpy as np
import random
import re
import string

# matrix for full vigene cipher --> save to external file
# full_chip_matrix = np.empty((26,26))
MAX_MATRIX_SIZE = 26
DECRYPTION_ERROR = "Please encrypt first before proceeding to decryption process"
DIVIDE_SIZE = 5

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
            random_char = random.choice(string.ascii_uppercase)
            if not random_char in key:
                key += random_char
    for item in key:
        selected_keys.append(list(item))
    
    while(len(selected_keys[0])<26):
        it = 0
        selected_chars = []
        random_char = ""
        for item in selected_keys:
            random_char = random.choice(string.ascii_uppercase)
            while (random_char in selected_chars or random_char in item):
                random_char = random.choice(string.ascii_uppercase)
            item += random_char
        # print(selected_keys)

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

def vigenere_running(text, opt):
    key = load_plain_text('pembukaanUUD1945.txt')
    return vigenere_standard(text, key, opt)

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

        rows = ""
        for char, temp_key in zip(temp_text, new_key):
            print(ord(temp_key)-65, ord(char)-65)
            rows+= str(ord(temp_key)-65) + ";"
            new_text += keys[ord(temp_key)-65][ord(char)-65]
        print(rows)
        print(new_text)
        save_file('keystore.txt', rows + "," + ''.join(temp))
    else:
        temp = load_plain_text('keystore.txt').split(",")
        keys = split_text(temp[1], 26)
        key_rows = temp[0].split(";")[0:-1]
        # print(key_rows)
        # print(keys)
        for char, temp_key in zip(temp_text, key_rows):
            # print(keys[int(temp_key)])
            idx = keys[int(temp_key)].index(char)
            new_text += chr(idx+65)
        print(new_text.lower())

def transpose_enc_dec(text, key, prev_key, opt):
    res = []
    if(opt == 0):
        diff = DIVIDE_SIZE - (len(key) % 5) 
        text += diff*'Z'
        # print(text)       
        temp = []
        # print(len(text)//DIVIDE_SIZE) 
        for i in range((len(text)//DIVIDE_SIZE)):
            temp.append( text[i*DIVIDE_SIZE:((i+1)*DIVIDE_SIZE)])
        # print(temp)
        for i in range(DIVIDE_SIZE):
            temp_str = ""
            for char in temp:
                temp_str += char[i]
            res.append(temp_str)
        return(''.join(res))
    else:
        mul = len(text)//DIVIDE_SIZE
        temp = []
        for i in range(DIVIDE_SIZE):
            temp.append(text[i*mul:((i+1)*mul)])
        # print(temp)
        for i in range(mul):
            temp_str = ""
            for char in temp:
                temp_str += char[i]
            res.append(temp_str)
        # print(key)
        # print(-(len(text)-len(prev_key)))
        # print(res)
        res_text = ''.join(res)
        final_res = res_text if (len(text)-len(prev_key) == 0) else res_text[:-(len(text)-len(prev_key))]
        return(final_res)    

def super_encrypt(text, key, opt):
    res = ""
    if(opt == 0):
        temp_text = clear_text(text).upper()
        new_key = generate_key_repeat(temp_text, key).upper()
        # print(new_key)
        save_file('temp_keystore.txt', new_key)
        temp = vigenere_standard(text, key, opt) 
        res = transpose_enc_dec(temp,new_key, new_key, opt)
    else:
        temp_text = clear_text(text).upper()
        new_key = generate_key_repeat(temp_text, key).upper()
        prev_key = load_plain_text('temp_keystore.txt')
        print(prev_key)
        temp_res = transpose_enc_dec(temp_text, new_key, prev_key, opt)
        res = vigenere_standard(temp_res, key, opt)
    return res

def inverse_modulo(m, n):
    for i in range(n):
        if ( (m * i) % n == 1 ):
            return i

def affine_cipher(text, key, opt):
    res = ""
    text = text.upper()
    # print(text)
    keys = key.split(" ")
    if(opt == 0):
        for i in range(len(text)):
            if(text[i] != ' '):
                res += chr(65 + ((ord(text[i])-65) * int(keys[0]) + int(keys[1])) % 26)
            else:
                res += ' '
    else:
        inv = inverse_modulo(int(keys[0]), 26)
        # print(inv)
        for i in range(len(text)):
            # print(inv, ord(text[i])-65, keys[1], (inv * (ord(text[i])-65 - int(keys[1]))))
            if(text[i] != ' '):
                res += chr(65 + (inv * (ord(text[i])-65 - int(keys[1]))) % 26)
            else:
                res += ' '

    # print(res.lower())
    return res.lower()

if __name__ == "__main__":
    # temp = load_plain_text("README.md")
    # print(temp)

    # print(vigenere_standard("LVVQHZNGFHRVL", "sonysonysonyss", 1))
    # print(generate_key_repeat("testtests", "test"))
    # print(generate_full_vigenere_key())
    # vigenere_full("OXAU", "temp", 1)
    # print(super_encrypt("MIIEEIIMMZ", "temp", 1))
    # print(affine_cipher("hkzo oxo oxfkh","7 10",1))