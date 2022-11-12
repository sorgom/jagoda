-- ============================================================
-- ### SAMPLE DATA
-- ============================================================
SET foreign_key_checks = 1;

-- Languages
REPLACE INTO LANG VALUES
    ('en', 'English',  0),
    ('de', 'Deutsch',  1),
    ('fr', 'Français', 2),
    ('hr', 'Hrvatski', 3)
;

-- Language element types
REPLACE INTO LANG_ITEM_TYPE VALUES
    ('OT', 'Object Titles', 1),
    ('CA', 'Website Captions', 0),
    ('TQ', 'Artpiece Techniques', 0)
;

-- Captions
REPLACE INTO LANG_ITEM VALUES
    (1, 'CA', 0),
    (2, 'CA', 0),
    (3, 'CA', 0),
    (4, 'CA', 0),
    (5, 'CA', 0),
    (6, 'CA', 0),
    (7, 'CA', 0),
    (8, 'CA', 0)
;

REPLACE INTO LANG_ELEM VALUES
    (1, 'en', 'Year'),
    (2, 'en', 'Exhibitions'),
    (3, 'en', 'Location'),
    (4, 'en', 'Owner'),
    (5, 'en', 'Artifact'),
    (6, 'en', 'Price'),
    (7, 'en', 'Search'),
    (8, 'en', 'Technique')
;

REPLACE INTO LANG_ITEM VALUES
    (20, 'CA', 0),
    (21, 'CA', 0),
    (22, 'CA', 0),
    (23, 'CA', 0),
    (24, 'CA', 0),
    (25, 'CA', 0)
;

REPLACE INTO LANG_ELEM VALUES
    (20, 'en', 'File'),
    (20, 'fr', 'Fiche'),
    (20, 'de', 'Datei'),
    (21, 'fr', 'Fántastique'),
    (22, 'en', 'This is a longer one in Englisch: let us see if it fits'),
    (23, 'de', 'This is a longer one in Deutsch: let us see if it fits'),
    (24, 'fr', 'This is a longer one in Français: let us see if it fits'),
    (25, 'hr', 'This is a longer one in Hrvatski: let us see if it fits')
;

-- Make
REPLACE INTO LANG_ITEM VALUES
    (31, 'TQ', 0),
    (32, 'TQ', 0),
    (33, 'TQ', 0),
    (34, 'TQ', 0),
    (35, 'TQ', 0),
    (36, 'TQ', 0),
    (37, 'TQ', 0)
;

REPLACE INTO LANG_ELEM VALUES
    (31, 'en', 'Book'),
    (32, 'en', 'Print'),
    (33, 'en', 'Skulpture'),
    (34, 'en', 'Oil on Canvas'),
    (35, 'en', 'Screen Print'),
    (36, 'en', 'Water Colour'),
    (37, 'en', 'Catalogue')
;



-- our only article
REPLACE INTO OBJECT(ID) VALUES
    (4711)
;

REPLACE INTO ARTICLE(ID) VALUES
    (4711)
;

-- Some Authors
CALL setUsr('Ilonka', 'ChangeMeSoon');
CALL setUsr('Wumpel', 'Test123');
CALL setUsr('test', 'tt');

--  Update Sequences
CALL initSeq();
