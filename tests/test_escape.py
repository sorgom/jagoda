from flask import escape

c = 'hello "world"//'
e = escape(c)

print('c:', c)
print('e:', e)
