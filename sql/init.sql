SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';
SET GLOBAL log_bin_trust_function_creators = 1;

-- ============================================================
-- ### TABLES
-- ============================================================
-- ## language support
-- ============================================================

-- language definitions
-- ILC, ISO Language Codes acc. to 
-- https://www.w3schools.com/tags/ref_language_codes.asp
DROP TABLE IF EXISTS LANG;
CREATE TABLE LANG (
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(64) NOT NULL,
    ORD INT NOT NULL,
    PRIMARY KEY (ILC),
    UNIQUE(ORD)
);

-- type of language element
-- T title
-- C caption
-- W what ist is
-- M make / techniqe of artpiece
DROP TABLE IF EXISTS BABL_TYPE;
CREATE TABLE BABL_TYPE (
    TP CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    PRIMARY KEY (TP)
);

-- language elements type assignment
DROP TABLE IF EXISTS BABL_ITEM;
CREATE TABLE BABL_ITEM (
    ID INT NOT NULL AUTO_INCREMENT,
    TP CHAR(2) NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (TP) REFERENCES BABL_TYPE(TP) ON DELETE CASCADE
);

-- all language dependent elements
DROP TABLE IF EXISTS BABL_ELEM;
CREATE TABLE BABL_ELEM (
    ID INT NOT NULL,
    ILC CHAR(2) NOT NULL DEFAULT 'en',
    LABEL VARCHAR(128) NOT NULL DEFAULT '',
    PRIMARY KEY (ID, ILC),
    FOREIGN KEY (ID) REFERENCES BABL_ITEM(ID) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE
);

-- ============================================================
-- ## content elements
-- ============================================================

-- physical objects
DROP TABLE IF EXISTS OBJECT;
CREATE TABLE OBJECT (
    ID INT NOT NULL,
    TITLE INT,
    DIM1 INT NOT NULL DEFAULT 0,
    DIM2 INT NOT NULL DEFAULT 0,
    DIM3 INT NOT NULL DEFAULT 0,
    LOC INT NOT NULL,
    PRIMARY KEY (ID), 
    FOREIGN KEY (TITLE) REFERENCES BABL_ITEM(ID) ON DELETE CASCADE
);

-- Article / Artifact
DROP TABLE IF EXISTS ARTICLE;
CREATE TABLE ARTICLE (
    ID INT NOT NULL,
    TITLE INT,
    WHAT INT,
    YEAR INT,
    CNT INT4 NOT NULL DEFAULT 1,
    VAL TINYINT(1) DEFAULT 0,
    PUB TINYINT(1) DEFAULT 0,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID)    REFERENCES OBJECT(ID)    ON DELETE CASCADE,
    FOREIGN KEY (WHAT)  REFERENCES BABL_ITEM(ID) ON DELETE CASCADE,
    FOREIGN KEY (TITLE) REFERENCES BABL_ITEM(ID) ON DELETE CASCADE
);

-- ============================================================
-- ## images
-- ============================================================

--  list of existing images
DROP TABLE IF EXISTS IMG;
CREATE TABLE IMG (
    ID  INT NOT NULL,
    PRIMARY KEY (ID)
);

-- object image assignment
DROP TABLE IF EXISTS OBJECT_IMG;
CREATE TABLE OBJECT_IMG (
    OBJECT INT NOT NULL,
    IMG INT NOT NULL,
    ORD INT NOT NULL DEFAULT 1,
    PRIMARY KEY (OBJECT, IMG),
    FOREIGN KEY (OBJECT) REFERENCES OBJECT(ID) ON DELETE CASCADE,
    FOREIGN KEY (IMG)    REFERENCES IMG(ID)    ON DELETE CASCADE
);

-- ============================================================
-- ## sequences
-- ============================================================
DROP TABLE IF EXISTS SEQ;
CREATE TABLE SEQ  
(  
    LABEL VARCHAR(16) NOT NULL,  
    NUM INT NOT NULL,
    PRIMARY KEY (LABEL)  
);

--  Authors
DROP TABLE IF EXISTS AUT;
CREATE TABLE AUT  
(  
    ID INT NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(32) NOT NULL,
    PASS VARCHAR(32) BINARY NOT NULL,
    PRIMARY KEY (ID),
    UNIQUE(NAME)  
) CHARACTER SET latin1;

-- ============================================================
-- ## PROCEDURES & FUNCTIONS
-- ============================================================
-- language support
-- ============================================================

-- language table
DROP PROCEDURE IF EXISTS getLangTable;
DELIMITER :)  
CREATE PROCEDURE getLangTable()  
BEGIN
    SELECT ILC, LABEL FROM LANG ORDER BY ORD;
END :)  
DELIMITER ;

-- Retrieve language element types
DROP PROCEDURE IF EXISTS getBablTpTable;
DELIMITER :)  
CREATE PROCEDURE getBablTpTable()  
BEGIN
    SELECT * FROM BABL_TYPE;
END :)  
DELIMITER ;

-- retrieve language element type label
DROP PROCEDURE IF EXISTS getBablTpLabel;
DELIMITER :)  
CREATE PROCEDURE getBablTpLabel(pTP CHAR(2))  
BEGIN
    SELECT LABEL FROM BABL_TYPE WHERE TP = pTP LIMIT 1;
END :)  
DELIMITER ;

-- retrieve type of a babl entry
DROP PROCEDURE IF EXISTS getBablTp;
DELIMITER :)  
CREATE PROCEDURE getBablTp(pID INT)  
BEGIN
    SELECT TP FROM BABL_ITEM WHERE ID = pID LIMIT 1;
END :)  
DELIMITER ;

-- create new babl item
DROP PROCEDURE IF EXISTS newBabl; 
DELIMITER :)  
CREATE PROCEDURE newBabl(pID INT, pTP CHAR(2))  
BEGIN
    INSERT INTO BABL_ITEM VALUES (pID, pTP);
END :)  
DELIMITER ;

-- retrieve all language elements of a type 
DROP PROCEDURE IF EXISTS getBablTable;
DELIMITER :)  
CREATE PROCEDURE getBablTable(pTP CHAR(2))  
BEGIN
    SELECT B.ID, B.ILC, B.LABEL 
    FROM BABL_ELEM as B
        INNER JOIN BABL_ITEM as T
        ON B.ID = T.ID 
        INNER JOIN LANG as L 
        ON B.ILC = L.ILC
    WHERE T.TP = pTP
    ORDER BY B.ID, L.ORD;
END :)  
DELIMITER ;

-- retrieve language element by ID
DROP PROCEDURE IF EXISTS getBabl; 
DELIMITER :)  
CREATE PROCEDURE getBabl(pID INT)  
BEGIN
    SELECT L.ILC, B.LABEL
    FROM BABL_ELEM as B INNER JOIN LANG as L 
    ON B.ILC = L.ILC 
    WHERE B.ID = pID
    ORDER BY L.ORD;
END :)  
DELIMITER ;


-- set language element
-- CALL setBabl(<id>, <ilc>, <label>);
DROP PROCEDURE IF EXISTS setBabl;
DELIMITER :)  
CREATE PROCEDURE setBabl(
    pID INT, 
    pILC CHAR(2), 
    pLABEL VARCHAR(128)) 
BEGIN
    IF pLABEL = '' THEN
        DELETE FROM BABL_ELEM WHERE ID = pID AND ILC = pILC;
    ELSE
        REPLACE INTO BABL_ELEM() VALUES (pID, pILC, pLABEL);
    END IF;
END :)  
DELIMITER ;

-- ============================================================
-- images
-- ============================================================
-- create new image element
DROP PROCEDURE IF EXISTS addImg;
DELIMITER :)  
CREATE PROCEDURE addImg(pID INT)
BEGIN
    REPLACE INTO IMG(ID) VALUES (pID);
END :)  
DELIMITER ;

-- create new objet image assignment
DROP PROCEDURE IF EXISTS addObjectImg;
DELIMITER :)  
CREATE PROCEDURE addObjectImg(pOBJECT INT, pIMG INT)
BEGIN
    DECLARE vORD INT;

    SELECT max(ORD) FROM OBJECT_IMG
    WHERE OBJECT = pOBJECT AND IMG = pIMG
    INTO @vORD;

    SET @vORD = IFNULL(@vORD, -1);
    SET @vORD = @vORD + 1;

    REPLACE INTO OBJECT_IMG VALUES (pOBJECT, pIMG, @vORD);
END :)  
DELIMITER ;

-- ============================================================
-- sequences
-- ============================================================
-- retrieve next sequence value:
DROP FUNCTION IF EXISTS nextSeq;  
DELIMITER :)  
CREATE FUNCTION nextSeq(pLABEL VARCHAR(16))
RETURNS INT
BEGIN  
    DECLARE vNUM INT;  

    SELECT NUM FROM SEQ WHERE (LABEL = pLABEL) INTO @vNUM;  

    SET @vNUM = @vNUM + 1;
    UPDATE SEQ SET NUM = @vNUM WHERE (LABEL = pLABEL);

    RETURN @vNUM;
END :)  
DELIMITER ;

-- Initialize Sequences Counters
-- CALL initSeq();
DROP PROCEDURE IF EXISTS initSeq;  
DELIMITER :)  
CREATE PROCEDURE initSeq()  
BEGIN
    DECLARE num INT;
    DELETE FROM SEQ; 

    -- OBJECT.ID
    SELECT max(ID) FROM OBJECT INTO @num;
    INSERT INTO SEQ VALUES ('OBJECT', IFNULL(@num, 0));

    -- BABL_ITEM.ID
    SELECT max(ID) FROM BABL_ITEM INTO @num;
    INSERT INTO SEQ VALUES ('BABL', IFNULL(@num, 0));

    -- IMG.ID
    SELECT max(ID) FROM IMG INTO @num;
    INSERT INTO SEQ VALUES ('IMG', IFNULL(@num, 0));

END :)  
DELIMITER ; 

-- Add / Modify an Author
-- CALL setAut(<name>, <password>);
DROP PROCEDURE IF EXISTS setAut;  
DELIMITER :)  
CREATE PROCEDURE setAut(pNAME VARCHAR(32), pPASS VARCHAR(32))  
BEGIN
    REPLACE INTO AUT (NAME, PASS) VALUES(LOWER(pNAME), MD5(pPASS));
END :)  
DELIMITER ;

-- Retrieve Author ID by Name and Password (MD5):
-- SELECT autId(<name>, <md5>);
DROP FUNCTION IF EXISTS autId;  
DELIMITER :)  
CREATE FUNCTION autId(pNAME VARCHAR(32), pMD5 VARCHAR(32))  
RETURNS INT
BEGIN  
    DECLARE vID INT;
    SET @vID = -1;  
    SELECT ID FROM AUT WHERE (NAME = LOWER(pNAME) AND PASS = pMD5) INTO @vID; 
    RETURN @vID;
END :)  
DELIMITER ;

-- Change Password of Author by ID
-- CALL setPass(<id>, <md5>);
DROP PROCEDURE IF EXISTS setPass;  
DELIMITER :)  
CREATE PROCEDURE setPass(pID INT, pMD5 VARCHAR(32)) 
BEGIN
    UPDATE AUT SET PASS = pMD5 WHERE ID = pID;
END :)  
DELIMITER ;

-- ============================================================
-- ## DATA
-- ============================================================
-- Languages
INSERT INTO LANG VALUES
    ('en', 'English',  0),
    ('de', 'Deutsch',  1),
    ('fr', 'Français', 2),
    ('hr', 'Hrvatski', 3)
;

-- Language element types
-- T title
-- C caption
-- W what ist is
-- M make / techniqe of artpiece
INSERT INTO BABL_TYPE(TP, LABEL) VALUES
    ('ST', 'Standard Titles'),
    ('CA', 'Website Captions'),
    ('TP', 'Element Types'),
    ('TQ', 'Artpiece Techniques')
;

-- Captions
INSERT INTO BABL_ITEM VALUES
    (1, 'CA'),
    (2, 'CA'),
    (3, 'CA'),
    (4, 'CA'),
    (5, 'CA'),
    (6, 'CA'),
    (7, 'CA'),
    (8, 'CA')
;

INSERT INTO BABL_ELEM(ID, LABEL) VALUES
    (1, 'Year'),
    (2, 'Exhibitions'),
    (3, 'Location'),
    (4, 'Owner'),
    (5, 'Artifact'),
    (6, 'Price'),
    (7, 'Search'),
    (8, 'Technique')
;

INSERT INTO BABL_ITEM VALUES
    (20, 'CA'),
    (21, 'CA'),
    (22, 'CA'),
    (23, 'CA'),
    (24, 'CA'),
    (25, 'CA')
;

INSERT INTO BABL_ELEM VALUES
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
INSERT INTO BABL_ITEM VALUES
    (31, 'TQ'),
    (32, 'TQ'),
    (33, 'TQ'),
    (34, 'TQ'),
    (35, 'TQ'),
    (36, 'TQ'),
    (37, 'TQ')
;

INSERT INTO BABL_ELEM(ID, LABEL) VALUES
    (31, 'Book'),
    (32, 'Print'),
    (33, 'Skulpture'),
    (34, 'Oil on Canvas'),
    (35, 'Screen Print'),
    (36, 'Water Colour'),
    (37, 'Catalogue')
;

-- our only article
INSERT INTO ARTICLE(ID) VALUES
    (4711)
;

-- Some Authors
CALL setAUT('Ilonka', 'ChangeMeSoon');
CALL setAUT('Wumpel', 'Test123');
CALL setAUT('test', 'tt');

--  Update Sequences
CALL initSeq();

-- ============================================================
-- ## Assigned Database Users
-- ============================================================

-- Author can change Content
DROP USER IF EXISTS 'aut'@'%';
CREATE USER 'aut'@'%' IDENTIFIED BY 'aa';
GRANT SELECT, INSERT, UPDATE, DELETE ON jagoda.* TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION  jagoda.nextSeq TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION  jagoda.autId   TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.setPass TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.newBabl TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.setBabl TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.initSeq TO 'aut'@'%';

-- TODO: user type: viewer with login

-- Web Visitor can just read
DROP USER IF EXISTS 'web'@'%';
CREATE USER 'web'@'%' IDENTIFIED BY 'ww';
GRANT SELECT ON jagoda.* TO 'web'@'%';

-- Everybody
GRANT EXECUTE ON PROCEDURE jagoda.getLangTable   TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getBablTpTable TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getBablTpLabel TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getBablTp      TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getBablTable   TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getBabl        TO 'aut'@'%', 'web'@'%';

-- ============================================================
-- Last Steps
-- ============================================================
SET foreign_key_checks = 1;
