# Language Object Model
## Language (LANG)
Definition of languages in use
- international language code (ilc)
	- see also [W3C HTML Language Code Reference](https://www.w3schools.com/tags/ref_language_codes.asp)
- native language label
- place within language priorities
## Titles and object captions
### Title (TTL)
A title
attributes
- is standard
- time stamp of last change
### Title element (TTL_ELEM)
A title element defining the content of a title in one of the languages 
refers:
- title
- language (ilc)
attributes:
- content VARCHAR(128)
## Long text
### Text (TXT)
A text
attributes
- time stamp of last change
## Text element (TXT_ELEM)
A description element defining the content of a description in one of the languages 
refers:
- text
- language (ilc)
attributes:
- content LONGTEXT
## Website captions (CAP)
A caption
attributes
- short keyword of caption used as place holder in websites
- time stamp of last change
### Caption element (CAP_ELEM)
A caption element defining the content of a caption in one of the languages 
refers:
- caption
- language (ilc)
attributes:
- content VARCHAR(128)
