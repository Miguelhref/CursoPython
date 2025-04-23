with open('./Python102/text.txt','r+') as file:
    for linea in file:
        print(linea)
    file.write('\ncosa nueva2')
