# google translate

## instalation
```
pip install googletrans==3.1.0a0
```
Hint:
**Update 06.12.20: A new 'official' alpha version of googletrans with a fix was released**

## usage sample
```
>>> from googletrans import Translator
>>> translator = Translator()
>>> res = translator.translate('Hello World', src='en', dest='hr')
>>> re.text
'Pozdrav svijete'
>>> 
```