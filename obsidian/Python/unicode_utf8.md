```python
import codecs

file = codecs.open(filename, 'w', 'utf-8')
file.write(u'\ufeff')
file.close()

with codecs.open(filename, 'r', 'utf-8') as fh:
    html = fh.read()
    fh.close()
```
