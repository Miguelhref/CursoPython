'''
from package.mod_1 import func_1,func_2
import package.mod_1
from package.mod_2 import func_3,func_4

print(func_1())
print(func_2())
print(func_3())
print(func_4())
'''

import package
print(package.URL)
print(package.mod_1.func_1())