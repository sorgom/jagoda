-- ============================================================
-- ### TABLES
-- ============================================================
-- Database collation: utf8mb4_bin

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';
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
-- Language element types
INSERT INTO LANG_ITEM_TYPE VALUES
    ('OT', 'Object Titles', 1),
    ('CA', 'Website Captions', 0),
    ('TQ', 'Artpiece Techniques', 0)
;

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
    TITLE BIGINT NOT NULL,
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
-- ============================================================
-- ## users
-- ============================================================
DROP TABLE IF EXISTS ROLE;
CREATE TABLE ROLE  
(  
    RC CHAR(1) NOT NULL,
    LABEL VARCHAR(8) NOT NULL,
    PRIMARY KEY (RC)
)  CHARACTER SET latin1;

INSERT INTO ROLE VALUES
    ('X', 'Author'),
    ('Y', 'Admin')
;

DROP TABLE IF EXISTS USR;
CREATE TABLE USR  
(  
    ID BIGINT NOT NULL AUTO_INCREMENT,
    NAME VARCHAR(32) NOT NULL,
    PASS VARCHAR(32) BINARY NOT NULL,
    RC CHAR(1) NOT NULL DEFAULT 'X',
    PRIMARY KEY (ID),
    FOREIGN KEY (RC) REFERENCES ROLE(RC) ON DELETE CASCADE 
) CHARACTER SET latin1;

-- ============================================================
-- ## Assigned Database Users
-- ============================================================
DELIMITER ;
-- Author can change Content
DROP USER IF EXISTS 'aut'@'%';
CREATE USER 'aut'@'%' IDENTIFIED BY 'aa';
GRANT SELECT, INSERT, UPDATE, DELETE ON jagoda.* TO 'aut'@'%';

-- TODO: user type: viewer with login

-- Web Visitor can just read
DROP USER IF EXISTS 'web'@'%';
CREATE USER 'web'@'%' IDENTIFIED BY 'ww';
GRANT SELECT ON jagoda.* TO 'web'@'%';

