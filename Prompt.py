#!/usr/bin/python3


print('Wild 0.1')
print('Type "help" if you need help. It will make you feel better.')
try:
    while(True):
      s = input('> ')
      print(s)

except EOFError:
    print('\n')
