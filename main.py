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



def PlayfairKeyMatrix(key=''):
    key = clear_text(key).upper()
    key = key.replace('J','')
    unique = []
    matrix = []

    for each in key:
        if not unique.count(each):
            unique.append(each)
    
    for each in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if not unique.count(each):
            unique.append(each)
    
    for i in range(5):
        row = []
        for j in range(5):
            row.append(unique[i*5+j])
        matrix.append(row)

    return matrix

def FindPositionMatrix(matrix = [[]], value = ''):
    x = 0
    y = 0
    for i in range(len(matrix)):
        if matrix[i].count(value):
            x = i
            y = matrix[i].index(value)

    return [x, y]

def PrintMatrix(matrix = [[]]):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if j:
                print(' ', end='')
            print(matrix[i][j], end='')
        print()

class Crypto():
    @staticmethod
    def PlayfairCipherEncrypt(plaintext='', key=''):
        matrix = PlayfairKeyMatrix(key)
        # PrintMatrix(matrix)
        plaintext = clear_text(plaintext).upper()
        bigram = []
        cipher = ''
        
        while plaintext:
            if len(plaintext) == 1:
                bigram.append(plaintext + 'X')
                plaintext = ''
            elif plaintext[0] == plaintext[1]:
                bigram.append(plaintext[0] + 'X')
                plaintext = plaintext[1:]
            else:
                bigram.append(plaintext[0:2])
                plaintext = plaintext[2:]
        # print(bigram)
        
        for i,each in enumerate(bigram):
            loc_first = FindPositionMatrix(matrix,each[0])
            loc_second = FindPositionMatrix(matrix,each[1])

            if i:
                cipher += ' '
            
            # RULES
            if loc_first[0] == loc_second[0]:
                if loc_first[1] == 4:
                    cipher += matrix[loc_first[0]][0]
                else:
                    cipher += matrix[loc_first[0]][loc_first[1]+1]

                if loc_second[1] == 4:
                    cipher += matrix[loc_second[0]][0]
                else:
                    cipher += matrix[loc_second[0]][loc_second[1]+1]
            elif loc_first[1] == loc_second[1]:
                if loc_first[0] == 4:
                    cipher += matrix[0][loc_first[1]]
                else:
                    cipher += matrix[loc_first[0]+1][loc_first[1]]

                if loc_second[0] == 4:
                    cipher += matrix[0][loc_second[1]]
                else:
                    cipher += matrix[loc_second[0]+1][loc_second[1]]
            else:
                cipher += matrix[loc_first[0]][loc_second[1]]
                cipher += matrix[loc_second[0]][loc_first[1]]
        
        return cipher

    @staticmethod
    def PlayfairCipherDecrypt(ciphertext='', key=''):
        matrix = PlayfairKeyMatrix(key)
        # PrintMatrix(matrix)
        ciphertext = ciphertext.split(' ')
        plainlist = []
        plaintext = ''
        
        for each in ciphertext:
            bigram = ''
            loc_first = FindPositionMatrix(matrix,each[0])
            loc_second = FindPositionMatrix(matrix,each[1])
            
            # RULES
            if loc_first[0] == loc_second[0]:
                if loc_first[1] == 0:
                    bigram += matrix[loc_first[0]][4]
                else:
                    bigram += matrix[loc_first[0]][loc_first[1]-1]

                if loc_second[1] == 0:
                    bigram += matrix[loc_second[0]][4]
                else:
                    bigram += matrix[loc_second[0]][loc_second[1]-1]
            elif loc_first[1] == loc_second[1]:
                if loc_first[0] == 0:
                    bigram += matrix[4][loc_first[1]]
                else:
                    bigram += matrix[loc_first[0]-1][loc_first[1]]

                if loc_second[0] == 0:
                    bigram += matrix[4][loc_second[1]]
                else:
                    bigram += matrix[loc_second[0]-1][loc_second[1]]
            else:
                bigram += matrix[loc_first[0]][loc_second[1]]
                bigram += matrix[loc_second[0]][loc_first[1]]

            plainlist.append(bigram)
            
        plainlist.reverse()
        removed = 0

        for each in plainlist:
            if plaintext:
                if each[0] == plaintext[0] and each[1] == 'X':
                    plaintext = each[0] + plaintext
                    removed += 1
                else:
                    plaintext = each + plaintext
            else:
                plaintext = each + plaintext
        
        if (len(plaintext)+removed) % 2 == 0:
            plaintext = plaintext[:-1]
        
        return plaintext

if __name__ == "__main__":
    # temp = load_plain_text("README.md")
    # print(temp)

    # print(vigenere_standard("LVVQHZNGFHRVL", "sonysonysonyss", 1))
    # print(generate_key_repeat("testtests", "test"))
    # print(generate_full_vigenere_key())
    vigenere_full("test", "temp", 0)