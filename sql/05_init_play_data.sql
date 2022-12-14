-- ============================================================
-- ### SAMPLE DATA
-- ============================================================
SET foreign_key_checks = 1;

-- Languages
REPLACE INTO LANG(ILC, LABEL, ORD) VALUES
    ('en', 'English',   0),
    ('hr', 'Hrvatski',  1),
    ('it', 'Italiano',  2),
    ('fr', 'Français',  3),
    ('de', 'Deutsch',   4),
    ('ko', '한국인',     5)
;

-- Make
delete from TTL where TPC = 'TQ' and ID < 1000;

INSERT INTO TTL(ID, TPC) VALUES
    (10, 'TQ'),
    (11, 'TQ'),
    (12, 'TQ'),
    (13, 'TQ'),
    (14, 'TQ'),
    (15, 'TQ'),
    (16, 'TQ'),
    (17, 'TQ'),
    (18, 'TQ'),
    (19, 'TQ')
;

insert INTO TTL_ELEM VALUES
    (10, 'en', 'sheet of paper'),
    (11, 'en', 'book'),
    (12, 'en', 'print'),
    (13, 'en', 'skulpture'),
    (14, 'en', 'oil on canvas'),
    (15, 'en', 'screen print'),
    (16, 'en', 'watercolour'),
    (17, 'en', 'catalogue'),
    (18, 'en', 'car'),
    (19, 'en', 'building')
;

-- website captions
-- moved to 06_gen_init_caps.sql

-- Some Authors
delete from USR;
insert into USR(ID, NAME, PASS) VALUES
    (1, 'ilonka', MD5('ChangeMeSoon')),
    (2, 'wumpel', MD5('Test123')),
    (3, 'test', MD5('tt'))
;
-- CALL setUsr('Ilonka', 'ChangeMeSoon');
-- CALL setUsr('Wumpel', 'Test123');
-- CALL setUsr('test', 'tt');

--  Update Sequences
CALL initSeq();
