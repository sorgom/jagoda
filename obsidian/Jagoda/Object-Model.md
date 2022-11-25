# Main object model
## Entity (ENT)
- can be owned
- can be somewhere
## Object (OBJ)
- inherits entity
- has dimensions
- has a title
- has one or more images
## Article (ART)
- inherits object
	- has several article / art piece specific atributes
- can be grouped
## Container (CON)
- inherits object
- can represent a standard container type
## LE-Element (LEE)
Element of a lilited edition
- inherits entity
- refers to article representing the limited edition

## Person / Instititution (PER)
- has
	- a name
	- telephone / cell phone
	- e-mail
- can have several locations
	- one (e.g. first) of whitch is main address
## Location (LOC)
- address
- telephone
## Person location (PER_LOC)
refers:
- person / institution
- location

## Ownership (PER_ENT)
unique relation of
- person / institiution
- entity
additional attribute
- amount
## Placement (LOC_ENT)
unique relation of
- location
- entity
additional attribute
- amount
## Exhibition (EXH)
refers:
- person / institution
- location
additional attributes
- start date
- end date
- title
## Assignment to exhibitions (EXH_ENT)
refers:
- entity
- exhibition
additional attribute
- amount

# Service object model
## User roles (ROL)
attributes
- role type
- label
TODO: label should become a caption
## User roles (ROL)
refers:
- roles
attributes
- ID
- usr name
- password md5

## Last changes to object (OBJ_REC)
refers:
- object
- user
additional attribute
- time stamp



