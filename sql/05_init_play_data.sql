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
REPLACE INTO TTL_TYPE VALUES
    ('OT', 'Object Titles', 1),
    ('CA', 'Website Captions', 0),
    ('TQ', 'Artpiece Techniques', 0)
;

-- Captions
REPLACE INTO TTL(ID, TPC) VALUES
    (1, 'CA'),
    (2, 'CA'),
    (3, 'CA'),
    (4, 'CA'),
    (5, 'CA'),
    (6, 'CA'),
    (7, 'CA'),
    (8, 'CA')
;

REPLACE INTO TTL_ELEM VALUES
    (1, 'en', 'Year'),
    (2, 'en', 'Exhibitions'),
    (3, 'en', 'Location'),
    (4, 'en', 'Owner'),
    (5, 'en', 'Artifact'),
    (6, 'en', 'Price'),
    (7, 'en', 'Search'),
    (8, 'en', 'Technique')
;

REPLACE INTO TTL(ID, TPC) VALUES
    (20, 'CA'),
    (21, 'CA'),
    (22, 'CA'),
    (23, 'CA'),
    (24, 'CA'),
    (25, 'CA')
;

REPLACE INTO TTL_ELEM VALUES
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
REPLACE INTO TTL(ID, TPC) VALUES
    (30, 'TQ'),
    (31, 'TQ'),
    (32, 'TQ'),
    (33, 'TQ'),
    (34, 'TQ'),
    (35, 'TQ'),
    (36, 'TQ'),
    (37, 'TQ'),
    (38, 'TQ'),
    (39, 'TQ')
;

REPLACE INTO TTL_ELEM VALUES
    (31, 'en', 'Sheet of Paper'),
    (31, 'en', 'Book'),
    (32, 'en', 'Print'),
    (33, 'en', 'Skulpture'),
    (34, 'en', 'Oil on Canvas'),
    (35, 'en', 'Screen Print'),
    (36, 'en', 'Water Colour'),
    (37, 'en', 'Catalogue'),
    (38, 'en', 'Car'),
    (39, 'en', 'Building')
;

-- Some Authors
CALL setUsr('Ilonka', 'ChangeMeSoon');
CALL setUsr('Wumpel', 'Test123');
CALL setUsr('test', 'tt');

--  Update Sequences
CALL initSeq();
