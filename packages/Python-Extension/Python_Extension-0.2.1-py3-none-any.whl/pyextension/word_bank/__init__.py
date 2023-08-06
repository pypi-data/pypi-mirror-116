# This document complies with the GPL open source agreement

import pickle
import os

word = {
    'a' : [
        'a',
        'able',
        'ability',
        'achivement',
        'again',
        'all',
        'alpha',
        'am',
        'an',
        'ant',
        'any',
        'angry',
        'anyone',
        'anybody',
        'anywhere',
        'apple',
        'apply',
        'application',
        'April',
        'are',
        'as',
        'aunt',
        'August',
        'awful',
        ''
        ],
    'b' : [
        'b',
        'bank',
        'base',
        'basic',
        'banana',
        'basket',
        'baseball',
        'basketball',
        'beach',
        'bit',
        'boom',
        'bring',
        'bridge',
        'bright',
        ''
        ],
    'c' : [
        'c',
        'car',
        'cake',
        'case',
        'cash',
        'canvas',
        'cabbage',
        'celebrate',
        'cell',
        'cute',
        ],
    'd' : [
        'd',
        'data',
        'date',
        'dance'
        'danger',
        'dangeons',
        ''
        ],
    'e' : [
        'e'
        ],
    'f' : [
        'f'
        ],
    'g' : [
        'g'
        ],
    'h' : [
        'h'
        ],
    'i' : [
        'i'
        ],
    'j' : [
        'j'
        ],
    'k' : [
        'k'
        ],
    'l' : [
        'l'
        ],
    'm' : [
        'm'
        ],
    'n' : [
        'n'
        ],
    'o' : [
        'o'
        ],
    'p' : [
        'p'
        ],
    'q' : [
        'q'
        ],
    'r' : [
        'r'
        ],
    's' : [
        's'
        ],
    't' : [
        't'
        ],
    'u' : [
        'u'
        ],
    'v' : [
        'v'
        ],
    'w' : [
        'w'
        ],
    'x' : [
        'x'
        ],
    'y' : [
        'y'
        ],
    'z' : [
        'z'
        ]
    }

def init():
    file = open('word bank.dat', 'wb')
    pickle.dump(word, file)
    file.close()
    return word
def search(key):
    file = open('word bank.dat', 'rb')
    dic = pickle.load(file)
    file.close()
    return dic[key]
def get():
    file = open('word bank.dat', 'rb')
    dic = pickle.load(file)
    file.close()
    return dic
def insert(dic, key, item):
    file = open('word bank.dat', 'rb')
    dic = pickle.load(file)
    file.close()
    if type(item) == type([]):
        for x in item:
            dic[key].append(x)
    else:
        raise TypeError('item must be list type')
    file = open('word bank.dat', 'wb')
    pickle.dump(dic, file)
    file.close()
    return dic
def change(dic, key, item):
    file = open('word bank.dat', 'rb')
    dic = pickle.load(file)
    file.close()
    if type(item) == type([]):
        dic[key] = item
    else:
        raise TypeError('item must be list type')
    file = open('word bank.dat', 'wb')
    pickle.dump(dic, file)
    file.close()
    return dic
def delete(dic, key, item):
    if type(item) == type(1):
        del dic[key][item]
    elif type(item) == type(''):
        times = 0
        try:
            while True:
                if dic[key][times] == item:
                    del dic[key][times]
                    break
                times += 1
        except IndexError:
            raise ValueError('No item \'%s\' in word bank.dat[%s]' % (item, key))
        return dic
    else:
        raise TypeError('type \'item\' must be string or int')
