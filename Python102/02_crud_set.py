set_countries = {'col','mex','bol'}
size = len(set_countries)
print(size)

print('col' in set_countries)
print('peru' in set_countries)

#add
set_countries.add('peru')
print('peru' in set_countries)

#update
set_countries.update({'ar','ecua','peru'})

print(set_countries)

#remove

set_countries.remove('col')
print(set_countries)

set_countries.remove('ar')
print(set_countries)

#vaciar

set_countries.clear()
print(set_countries)



