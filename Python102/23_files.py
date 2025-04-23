file = open('./Python102/text.txt')
#print(file.read())
#print(file.readline())

for linea in file:
    print(linea)

file.close()

with open('./Python102/text.txt') as file:
    for line in file:
        print (line)