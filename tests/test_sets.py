

set1 = {1, 2, 3, 4, 5, 6, 7, 20}
set2 = {2, 4, 6, 8, 20}
set3 = {33, 44, 55}

setInt = set1.intersection(set2)
print('setInt', setInt)

setDif = set1.difference(set2)
print('setDif', setDif)

if set1.intersection(set3):
    print('common')
else:
    print('no common')

