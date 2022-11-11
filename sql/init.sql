-- Database collation: utf8mb4_bin

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';
-- enables funtions / procedures that don't acces any tables:
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

-- possible type of language item
DROP TABLE IF EXISTS LANG_ITEM_TYPE;
CREATE TABLE LANG_ITEM_TYPE (
    TPC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    STDABLE TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (TPC)
);

-- language item of a type
DROP TABLE IF EXISTS LANG_ITEM;
CREATE TABLE LANG_ITEM (
    ID BIGINT NOT NULL,
    TPC CHAR(2) NOT NULL,
    STD TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (ID),
    FOREIGN KEY (TPC) REFERENCES LANG_ITEM_TYPE(TPC) ON DELETE CASCADE
);

-- language dependent element
-- language item for all languages
DROP TABLE IF EXISTS LANG_ELEM;
CREATE TABLE LANG_ELEM (
    ID BIGINT NOT NULL,
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    PRIMARY KEY (ID, ILC),
    FOREIGN KEY (ID) REFERENCES LANG_ITEM(ID) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE
);

-- ============================================================
-- ## content elements
-- ============================================================

-- physical objects
DROP TABLE IF EXISTS OBJECT;
CREATE TABLE OBJECT (
    ID BIGINT NOT NULL,
    TITLE BIGINT,
    DIM1 INT NOT NULL DEFAULT 0,
    DIM2 INT NOT NULL DEFAULT 0,
    DIM3 INT NOT NULL DEFAULT 0,
    LOC BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (ID), 
    FOREIGN KEY (TITLE) REFERENCES LANG_ITEM(ID) ON DELETE CASCADE
);

-- article / artifact
DROP TABLE IF EXISTS ARTICLE;
CREATE TABLE ARTICLE (
    ID BIGINT NOT NULL,
    WHAT BIGINT,
    YEAR INT,
    CNT INT4 NOT NULL DEFAULT 1,
    VAL TINYINT(1) DEFAULT 0,
    PUB TINYINT(1) DEFAULT 0,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID)    REFERENCES OBJECT(ID)    ON DELETE CASCADE,
    FOREIGN KEY (WHAT)  REFERENCES LANG_ITEM(ID) ON DELETE CASCADE
);

-- ============================================================
-- ## images
-- ============================================================

--  list of existing images
DROP TABLE IF EXISTS IMG;
CREATE TABLE IMG (
    ID BIGINT NOT NULL,
    PRIMARY KEY (ID)
);

-- object image assignment
DROP TABLE IF EXISTS OBJECT_IMG;
CREATE TABLE OBJECT_IMG (
    OBJECT BIGINT NOT NULL,
    IMG BIGINT NOT NULL,
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
    ID TINYINT NOT NULL,
    NUM BIGINT NOT NULL,
    PRIMARY KEY (ID)
);
INSERT INTO SEQ VALUES(1, 0);

--  Authors
DROP TABLE IF EXISTS AUT;
CREATE TABLE AUT  
(  
    ID BIGINT NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(32) NOT NULL,
    PASS VARCHAR(32) BINARY NOT NULL,
    PRIMARY KEY (ID),
    UNIQUE(NAME)  
) CHARACTER SET latin1;

-- ============================================================
-- ## PROCEDURES & FUNCTIONS
-- ============================================================
-- sequences
-- ============================================================
-- retrieve next id sequence value:
DROP FUNCTION IF EXISTS nextId;  
DELIMITER :)  
CREATE FUNCTION nextId()
RETURNS BIGINT
BEGIN  
    DECLARE vNUM BIGINT;  
    SELECT NUM FROM SEQ WHERE (ID = 1) INTO @vNUM; 
    SET @vNUM = IFNULL(@vNUM, 0) + 1;
    REPLACE INTO SEQ VALUES(1, @vNUM);
    RETURN @vNUM;
END :)  
DELIMITER ;

-- initialize sequences counters
DROP PROCEDURE IF EXISTS initSeq;  
DELIMITER :)  
CREATE PROCEDURE initSeq()  
BEGIN
    DECLARE num BIGINT;
    SELECT GREATEST(
    -- OBJECT.ID
         IFNULL((SELECT MAX(ID) FROM OBJECT), 0),
    -- LANG_ITEM.ID
         IFNULL((SELECT MAX(ID) FROM LANG_ITEM), 0),
    -- IMG.ID
         IFNULL((SELECT MAX(ID) FROM IMG), 0)
    --  TODO
        -- CONT.ID
        -- GRP.ID
    ) INTO @num;
    REPLACE INTO SEQ VALUES(1, @num);
END :)  
DELIMITER ;

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

-- retrieve language element types
DROP PROCEDURE IF EXISTS getLangItemTypeTable;
DELIMITER :)  
CREATE PROCEDURE getLangItemTypeTable()
BEGIN
    SELECT * FROM LANG_ITEM_TYPE;
END :)  
DELIMITER ;

-- retrieve language element type label
DROP PROCEDURE IF EXISTS getLangItemTypeLabel;
DELIMITER :)  
CREATE PROCEDURE getLangItemTypeLabel(pTP CHAR(2))  
BEGIN
    SELECT LABEL FROM LANG_ITEM_TYPE WHERE TPC = pTP LIMIT 1;
END :)  
DELIMITER ;

-- retrieve type of a language item
DROP PROCEDURE IF EXISTS getLangItemType;
DELIMITER :)  
CREATE PROCEDURE getLangItemType(pID BIGINT)  
BEGIN
    SELECT TPC FROM LANG_ITEM WHERE ID = pID LIMIT 1;
END :)  
DELIMITER ;

-- create new language item
DROP PROCEDURE IF EXISTS newLangItem; 
DELIMITER :)  
CREATE PROCEDURE newLangItem(pID BIGINT, pTP CHAR(2))  
BEGIN
    INSERT INTO LANG_ITEM VALUES (pID, pTP);
END :)  
DELIMITER ;

-- retrieve all language elements of a type 
DROP PROCEDURE IF EXISTS getLangElemTable;
DELIMITER :)  
CREATE PROCEDURE getLangElemTable(pTPC CHAR(2))  
BEGIN
    SELECT E.ID, E.ILC, E.LABEL 
    FROM LANG_ELEM as E
        INNER JOIN LANG_ITEM as I
        ON E.ID = I.ID 
        INNER JOIN LANG as L 
        ON E.ILC = L.ILC
    WHERE I.TPC = pTPC
    ORDER BY E.ID, L.ORD;
END :)  
DELIMITER ;

-- retrieve language element by ID
DROP PROCEDURE IF EXISTS getLangElem; 
DELIMITER :)  
CREATE PROCEDURE getLangElem(pID BIGINT)  
BEGIN
    SELECT L.ILC, E.LABEL
    FROM LANG_ELEM as E INNER JOIN LANG as L 
    ON E.ILC = L.ILC 
    WHERE E.ID = pID
    ORDER BY L.ORD;
END :)  
DELIMITER ;


-- set language element
DROP PROCEDURE IF EXISTS setLangElem;
DELIMITER :)  
CREATE PROCEDURE setLangElem(
    pID BIGINT, 
    pILC CHAR(2), 
    pLABEL VARCHAR(128)) 
BEGIN
    IF pLABEL = '' THEN
        DELETE FROM LANG_ELEM WHERE ID = pID AND ILC = pILC;
    ELSE
        REPLACE INTO LANG_ELEM VALUES (pID, pILC, pLABEL);
    END IF;
END :)  
DELIMITER ;

-- ============================================================
-- objects
-- ============================================================
DROP FUNCTION IF EXISTS isObject;  
DELIMITER :)  
CREATE FUNCTION isObject(pID BIGINT)
RETURNS INT
BEGIN  
    DECLARE vNUM INT;  
    SELECT COUNT(*) FROM OBJECT WHERE (ID = pID) INTO @vNUM;  
    RETURN @vNUM;
END :)  
DELIMITER ;

-- ============================================================
-- images
-- ============================================================
DROP FUNCTION IF EXISTS imgPath;  
DROP FUNCTION IF EXISTS imgFileMini;  
DROP FUNCTION IF EXISTS imgFileFull;  
DROP FUNCTION IF EXISTS imgFileExif;
DROP PROCEDURE IF EXISTS imgFiles;
DROP PROCEDURE IF EXISTS imgFolders;

DELIMITER :)  
CREATE FUNCTION imgPath(pSUB VARCHAR(8), pID BIGINT, pEXT VARCHAR(4))
RETURNS VARCHAR(32)
BEGIN
    IF pID = -1 THEN 
        RETURN CONCAT('static/img/',  pSUB);
    ELSE 
        RETURN CONCAT('static/img/',  pSUB, '/', LPAD(pID, 7, 0), '.', pEXT);
    END IF;
END :)  
CREATE FUNCTION imgFileMini(pID BIGINT)
RETURNS VARCHAR(32)
BEGIN
    RETURN imgPath('mini', pID, 'jpg');
END :)  
CREATE FUNCTION imgFileFull(pID BIGINT)
RETURNS VARCHAR(32)
BEGIN
    RETURN imgPath('full', pID, 'jpg');
END :)  
CREATE FUNCTION imgFileExif(pID BIGINT)
RETURNS VARCHAR(32)
BEGIN
    RETURN imgPath('exif', pID, 'json');
END :)  
CREATE PROCEDURE imgFiles(pID BIGINT)
BEGIN
    SELECT imgFileMini(pID), imgFileFull(pID), imgFileExif(pID);
END :)
CREATE PROCEDURE imgFolders()
BEGIN
    CALL imgFiles(-1);
END :)
DELIMITER ;

DROP PROCEDURE IF EXISTS addImg;
DROP PROCEDURE IF EXISTS addObjectImg;
DROP PROCEDURE IF EXISTS getObjectImgs;
DROP PROCEDURE IF EXISTS setObjectImg;
DROP PROCEDURE IF EXISTS rmObjectImg;
DROP FUNCTION IF EXISTS getNumObjectImgs;  
DROP PROCEDURE IF EXISTS getUnusedImgs;

DELIMITER :)  
-- create new image element
CREATE PROCEDURE addImg(pID BIGINT)
BEGIN
    REPLACE INTO IMG(ID) VALUES (pID);
END :)  
-- create new objet image assignment
CREATE PROCEDURE addObjectImg(pOBJECT BIGINT, pIMG BIGINT)
BEGIN
    DECLARE vORD INT;

    REPLACE INTO IMG VALUES(pIMG); 
    
    SELECT MAX(ORD) FROM OBJECT_IMG
    WHERE OBJECT = pOBJECT
    INTO @vORD;

    SET @vORD = IFNULL(@vORD, -1);
    SET @vORD = @vORD + 1;

    REPLACE INTO OBJECT_IMG VALUES (pOBJECT, pIMG, @vORD);
END :)  
-- retrieve all images of an object
CREATE PROCEDURE getObjectImgs(pOBJECT BIGINT)
BEGIN
    SELECT IMG, ORD, imgFileMini(IMG) FROM OBJECT_IMG
    WHERE OBJECT = pOBJECT
    ORDER BY ORD;
END :)  
-- alter object image assignment
CREATE PROCEDURE setObjectImg(pOBJECT BIGINT, pIMG BIGINT, pORD INT)
BEGIN
    REPLACE INTO OBJECT_IMG VALUES (pOBJECT, pIMG, pORD);
END :)  
-- remove image from object
CREATE PROCEDURE rmObjectImg(pOBJECT BIGINT, pIMG BIGINT)
BEGIN
    DELETE FROM OBJECT_IMG WHERE OBJECT = pOBJECT AND IMG = pIMG;
END :)  
-- TODO: do we need this?
-- CREATE FUNCTION getNumObjectImgs(pOBJECT BIGINT)
-- RETURNS INT
-- BEGIN  
--     DECLARE vNUM INT;  
--     SELECT COUNT(*) FROM OBJECT_IMG WHERE (OBJECT = pOBJECT) INTO @vNUM;  
--     RETURN @vNUM;
-- END :)  
-- retrieve all unassigned images
CREATE PROCEDURE getUnusedImgs()
BEGIN
    SELECT I.ID, imgFileMini(I.ID) FROM IMG AS I
    LEFT JOIN  OBJECT_IMG AS OI 
    ON OI.IMG = I.ID
    WHERE OI.IMG IS NULL
    ORDER BY I.ID;
END :)  
DELIMITER ;

-- ============================================================
-- authors / users
-- ============================================================
-- add / modify an Author
DROP PROCEDURE IF EXISTS setUsr;  
DELIMITER :)  
CREATE PROCEDURE setUsr(pNAME VARCHAR(32), pPASS VARCHAR(32))  
BEGIN
    REPLACE INTO AUT (NAME, PASS) VALUES(LOWER(pNAME), MD5(pPASS));
END :)  
DELIMITER ;

-- retrieve author ID by name and password (MD5):
DROP FUNCTION IF EXISTS getUsrId;  
DELIMITER :)  
CREATE FUNCTION getUsrId(pNAME VARCHAR(32), pMD5 VARCHAR(32))  
RETURNS BIGINT
BEGIN  
    DECLARE vID BIGINT;
    SET @vID = -1;  
    SELECT ID FROM AUT WHERE (NAME = LOWER(pNAME) AND PASS = pMD5) INTO @vID; 
    RETURN @vID;
END :)  
DELIMITER ;

-- change password of author by ID
DROP PROCEDURE IF EXISTS setPass;  
DELIMITER :)  
CREATE PROCEDURE setPass(pID BIGINT, pMD5 VARCHAR(32)) 
BEGIN
    UPDATE AUT SET PASS = pMD5 WHERE ID = pID;
END :)  
DELIMITER ;


-- ============================================================
-- ## Assigned Database Users
-- ============================================================

-- Author can change Content
DROP USER IF EXISTS 'aut'@'%';
CREATE USER 'aut'@'%' IDENTIFIED BY 'aa';
GRANT SELECT, INSERT, UPDATE, DELETE ON jagoda.* TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION   jagoda.nextId                 TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.initSeq                TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.getLangTable           TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.getLangItemTypeTable   TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.getLangItemTypeLabel   TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.getLangItemType        TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.newLangItem            TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.getLangElemTable       TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.getLangElem            TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.setLangElem            TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION   jagoda.isObject               TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION   jagoda.imgPath                TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION   jagoda.imgFileMini            TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION   jagoda.imgFileFull            TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION   jagoda.imgFileExif            TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.imgFiles               TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.imgFolders             TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.addImg                 TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.addObjectImg           TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.getObjectImgs          TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.setObjectImg           TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.rmObjectImg            TO 'aut'@'%';
-- GRANT EXECUTE ON FUNCTION   jagoda.getNumObjectImgs       TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.getUnusedImgs          TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.setUsr                 TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION   jagoda.getUsrId               TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE  jagoda.setPass                TO 'aut'@'%';

-- TODO: user type: viewer with login

-- Web Visitor can just read
DROP USER IF EXISTS 'web'@'%';
CREATE USER 'web'@'%' IDENTIFIED BY 'ww';
GRANT SELECT ON jagoda.* TO 'web'@'%';

-- Everybody
GRANT EXECUTE ON PROCEDURE jagoda.getLangTable          TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangItemTypeTable  TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangItemTypeLabel  TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangItemType       TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangElemTable      TO 'aut'@'%', 'web'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangElem           TO 'aut'@'%', 'web'@'%';

-- ============================================================
-- ## DATA
-- ============================================================
SET foreign_key_checks = 1;

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
INSERT INTO LANG_ITEM_TYPE VALUES
    ('OT', 'Object Titles', 1),
    ('CA', 'Website Captions', 0),
    ('TQ', 'Artpiece Techniques', 0)
;

-- Captions
INSERT INTO LANG_ITEM VALUES
    (1, 'CA'),
    (2, 'CA'),
    (3, 'CA'),
    (4, 'CA'),
    (5, 'CA'),
    (6, 'CA'),
    (7, 'CA'),
    (8, 'CA')
;

INSERT INTO LANG_ELEM VALUES
    (1, 'en', 'Year'),
    (2, 'en', 'Exhibitions'),
    (3, 'en', 'Location'),
    (4, 'en', 'Owner'),
    (5, 'en', 'Artifact'),
    (6, 'en', 'Price'),
    (7, 'en', 'Search'),
    (8, 'en', 'Technique')
;

INSERT INTO LANG_ITEM VALUES
    (20, 'CA'),
    (21, 'CA'),
    (22, 'CA'),
    (23, 'CA'),
    (24, 'CA'),
    (25, 'CA')
;

INSERT INTO LANG_ELEM VALUES
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
INSERT INTO LANG_ITEM VALUES
    (31, 'TQ'),
    (32, 'TQ'),
    (33, 'TQ'),
    (34, 'TQ'),
    (35, 'TQ'),
    (36, 'TQ'),
    (37, 'TQ')
;

INSERT INTO LANG_ELEM VALUES
    (31, 'en', 'Book'),
    (32, 'en', 'Print'),
    (33, 'en', 'Skulpture'),
    (34, 'en', 'Oil on Canvas'),
    (35, 'en', 'Screen Print'),
    (36, 'en', 'Water Colour'),
    (37, 'en', 'Catalogue')
;

-- our only article
INSERT INTO OBJECT(ID) VALUES
    (4711)
;

INSERT INTO ARTICLE(ID) VALUES
    (4711)
;

-- Some Authors
CALL setAUT('Ilonka', 'ChangeMeSoon');
CALL setAUT('Wumpel', 'Test123');
CALL setAUT('test', 'tt');

--  Update Sequences
CALL initSeq();
