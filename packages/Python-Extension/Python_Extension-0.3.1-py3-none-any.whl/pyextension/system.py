import platform as p
import sys

def computer():
    print('===== %s =====' % p.node())
    print('''OS:
    %s''' % p.system())
    print('''Processor:
    %s''' % p.processor())
    print('''Machine:
    %s''' % p.machine())
    print('''Release:
    %s''' % p.release())
    print('''Platform:
    %s''' % p.platform())
    print('''Version:
    %s''' % p.version())

def python():
    print('===== Python ' + str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2]) + ' =====')
    print('''Version : ''')
    print(4 * ' ',end='')
    print(sys.version)
    print('''Build :
    ''',end='')
    print(p.python_build())
