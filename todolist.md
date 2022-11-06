# ideas / concepts
## containers and boxes
- dimensions
- standard containers / boxes

## Considerations
### all ids are unique
  - everything can be identified by ID
  - only one sequenz
  - only one table elment
### element types:
- physical types
  - have dimensions
  - can be made pictures of
  - can be searched for by ID / QRCode
  - can be assigned to abstract types
  - can be put into a container
  - e.g.:
    - art pieces
    - containers
  - a fit into another can be applied  
- abstract types: grouping
  - e.g.:
    - series
    - grouping for presentation
    - exhibitions?
### attributes
#### art pieces
  - title
  - image(s)
  - owner
  - author
  - price
  - dimensions
  - amount
    - can be splittet to different locations
  - origin location
  - current location
  - assignments to abstract types
    - if part of a series
      - same title, but different number within series
        - image of each individual required?

# TODO
## css
- input validity:
  - https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation 
- freeze table head

## js
- find all required / invalid form elements
    - partially done
- resize event
- keybord evaluation
- submit without submit (doesn' work)

## html
- keybord evaluation to element

## general
- image / thumbnail sizes from db
- establish roles
- check by array: babl types (not necessary due to MySQL constraints)
- js check required
- the application session secret has to be set in MySQL DB by root

## image processing
- limit number of images

# doing

# found out
## MySQL
- VARCHAR does not take longer strings
## Flask
- timer call within class does not work
- escape outgoing html texts not neccessary, done by render_template


# DONE
- post a form via ajax
- reposition element by window position (vertically)
- switch to open cv: NO Way!
- img subdirectory linked
- folder check
- pre-checks: dirs
