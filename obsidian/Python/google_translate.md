# google translate

## instalation
```shell
pip install googletrans==3.1.0a0
```
Hint:
*Update 06.12.20: A new 'official' alpha version of googletrans with a fix was released*

## usage sample
```python
>>> from googletrans import Translator
>>> translator = Translator()
>>> res = translator.translate('Hello World', src='en', dest='hr')
>>> re.text
'Pozdrav svijete'
>>> 
```

See also: [Googletrans: Free and Unlimited Google translate API for Python](https://py-googletrans.readthedocs.io/en/latest/)

