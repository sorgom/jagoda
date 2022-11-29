# Main object model
## Object (OBJ)
- inherits entity
- has dimensions
- has a title
- has one or more images
## Article (ART)
- inherits object
	- has several article / art piece specific attributes
- can be grouped
## Container (CON)
- inherits object
- can represent a standard container type
## Person / institution (PER)
- has
	- a name (can be different in different languages)
	- additional information, e.g.
		- telephone / cell phone
		- e-mail
- can have several locations
	- one (e.g. first) of witch is main address
## Location (LOC)
- address (can be different by language)
- telephone
## Person locations (PER_LOC)
refers:
- person / institution
- location
additional attribute
- order / main

## Ownership (PER_OBJ)
unique relation of
- person / institution
- object
additional attribute
- amount or numbers
## Placement (LOC_OBJ)
unique relation of
- location
- entity
additional attribute
- amount or numbers
## Exhibition (EXH)
refers:
- person / institution
- location
additional attributes
- start date
- end date
- title
## Assignment to exhibitions (EXH_OBJ)
refers:
- object
- exhibition
additional attribute
- amount or numbers

# Service object model
## User roles (ROL)
attributes
- role type
- label
## User (USR)
refers:
- roles
attributes
- ID
- user name
- password md5

## Last changes to object (OBJ_REC)
refers:
- object
- user
additional attribute
- time stamp



