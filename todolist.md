# current
- locations, persons / institution, addresses

# remeber
- search
  - implement search
    - recent
    - make
    - groups
  - save user search as JSON
- limited edition as an own table / object class

# done
- object title editor
- object selector (popup)
  - similar std title selector _lang_items
- gimmik: 
  - rename template script  
  - qrcode
    - close on print / printpopup()
    - alternative: just print, don't popup
- all sorts of updates must update object concerned
  - image assignement
  - title changes


2022-11-18
- lang items with timestamp
- dimensions form

2022-11-19
- make navigation safe:
  - JS: popupReplace



# ideas / concepts
## containers and boxes
- dimensions
- standard containers / boxes
## language support
- import / export: excel


## Considerations
- messaging: who edits what
  - general ajax message lookup
  - install agents who get informed by item id after updates / changes
### language support
#### website captions
- pre-defined / own class
- linked to shortcut names like FILE, OWN
- cannot be removed / added
- called by short
- own editor
- view only rights

### all ids are unique
- everything can be identified by ID
- only one sequenz
  - only one table elment
- alternative: ID contaims type of element
  - identification just by ID
### imaging
- recently added imgages
  - save addition date
- does it make sense to save originals?
  - make it a config entry?
- save image exif
  - let's see the performance: get exif from mini
  - exif should be kept private
    - save separate exif mini with nearly no size? => exif folder?
    - but copyrigth displayed?
    - general copyrights disclaimer?
    - set copyright generally?
  - SIMPLE SOLUTION: safe exif as JSON
- duplicate detection: save md5 / sha hash of full size thumbnail or original
  - use io.BytesIO for this
  - use pre-defined similarity definitions?
```
import io
from PIL import Image

im = Image.open('test.jpg')
im_resize = im.resize((500, 500))
buf = io.BytesIO()
im_resize.save(buf, format='JPEG')
byte_im = buf.getvalue()

```
  - alternatively: check python / PIP similarity features
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
- check: valid response on chrome

## css
- input validity:
  - https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation 
- freeze table head

## js
- DONE: find all required / invalid form elements
- resize event
- keybord evaluation
- DONE: submit without submit (doesn' work)
- multiple popup levels

## html
- keybord evaluation to element

## general
- image / thumbnail sizes from db
- establish roles
- check by array: babl types (not necessary due to MySQL constraints)
- js check required
- the application session secret has to be set in MySQL DB by root

## image processing
- DONE: limit number of images

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
