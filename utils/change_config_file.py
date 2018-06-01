import os
import sys
import fileinput

CONFIG_DICT = {
    'filename': '',
    'text_to_search': '',
}

filename  = '/etc/postfix/main.cf'
text_to_search = 'localhost.localdomain, '

print ("Text to replace it with:")
replacement_text = text_to_search +  str(input( "> " ) + ', ')

with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(text_to_search, replacement_text), end='')