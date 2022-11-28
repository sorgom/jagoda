```python
TEXTO = sys.argv[1]
my_regex = r"\b(?=\w)" + re.escape(TEXTO) + r"\b(?!\w)"

if re.search(my_regex, subject, re.IGNORECASE):
```

```python
rx = re.compile(f'^(-- GENERATED {what}>).*\n(-- <GENERATED {what})', re.M | re.S)
return rx.sub(r'\1\n' + '\n'.join(data) + r'\n\2', txt)
```

