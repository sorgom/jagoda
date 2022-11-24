# Object model
## Entity
- can be owned
- can be somewhere
## Object
- inherits entity
- has dimensions
- has a title
- has one or more images
## Article
- inherits object
	- has several article / art piece specific atributes
- can be grouped
## Container
- inherits object
- can represent a standard container type
## LE-Element
Element of a lilited edition
- inherits entity
- refers to article representing the limited edition

## Person / Instititution
- has
	- a name
	- telephone / cell phone
	- e-mail
- can have several locations
	- one (e.g. first) of whitch is main address
## Location
- address
- telephone
## Ownership
unique relation of
- person / institiution
- entity
additional attribute
- amount
## Placement
unique relation of
- location
- entity
additional attribute
- amount



