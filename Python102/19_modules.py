import sys
#print (sys.path)

import re
text = 'Mi numero de telefono es 311 123 121,' \
' el codigo del pais es 57, ' \
'mi numero de la suerte es 3'

result = re.findall('[0-9]+',text)
print(result)

import time
timestamp = time.time()
local_time = time.localtime()
result = time.asctime(local_time)
print(timestamp)
print(result)

import collections
numeros = [1,1,2,1,2,4,5,3,3,21]
counter = collections.Counter(numeros)
print(counter)