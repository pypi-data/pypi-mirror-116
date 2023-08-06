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

def init(value=None):
    return word
def search(value, key):
    return dic[key]
def get(value):
    return dic
def insert(dic, key, item):
    dic[key] = dic[key].append(item)
    return dic
def change(dic, key, item):
    if type(item) == type([]):
        dic[key] = item
    else:
        raise TypeError('Argument \'item\' must be list type')
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
