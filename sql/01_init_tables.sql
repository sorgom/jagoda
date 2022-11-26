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

-- 
DROP TABLE IF EXISTS ENT;
CREATE TABLE ENT (
    ID BIGINT NOT NULL,
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    PRIMARY KEY (ID),
);

-- language definitions
-- ILC, ISO Language Codes acc. to 
-- https://www.w3schools.com/tags/ref_language_codes.asp
DROP TABLE IF EXISTS LANG;
CREATE TABLE LANG ( -- ROOT
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(64) NOT NULL,
    ORD INT NOT NULL,
    PRIMARY KEY (ILC),
    UNIQUE(ORD)
);

-- title / object caption
DROP TABLE IF EXISTS TTL;
CREATE TABLE TTL (
    ENT BIGINT NOT NULL,
    STD TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (ENT),
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE
);

-- TTL element for all languages
DROP TABLE IF EXISTS TTL_ELEM;
CREATE TABLE TTL_ELEM (
    TNT BIGINT NOT NULL,
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    PRIMARY KEY (ENT, ILC),
    FOREIGN KEY (TNT) REFERENCES TTL(ENT) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE
);

-- long text descriptions
DROP TABLE IF EXISTS TXT;
CREATE TABLE TXT (
    ENT BIGINT NOT NULL,
    PRIMARY KEY (ENT),
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE
);

-- TXT element for all languages
DROP TABLE IF EXISTS TXT_ELEM;
CREATE TABLE TXT_ELEM (
    ENT BIGINT NOT NULL,
    ILC CHAR(2) NOT NULL,
    CONT LONGTEXT,
    PRIMARY KEY (ENT, ILC),
    FOREIGN KEY (ENT) REFERENCES TXT(ENT) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE
);

-- website captions
DROP TABLE IF EXISTS CAP;
CREATE TABLE CAP (
    ENT BIGINT NOT NULL,
    CPC VARCHAR(16) NOT NULL,
    PRIMARY KEY (ENT),
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE
);

-- CAP element for all languages
DROP TABLE IF EXISTS CAP_ELEM;
CREATE TABLE CAP_ELEM (
    ENT BIGINT NOT NULL,
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    PRIMARY KEY (ENT, ILC),
    FOREIGN KEY (ENT) REFERENCES CAP(ENT) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE
);


-- ============================================================
-- ## content elements
-- ============================================================

-- physical objects
DROP TABLE IF EXISTS OBJ;
CREATE TABLE OBJ (
    ENT BIGINT NOT NULL,
    TTL BIGINT NOT NULL,
    -- dimensions in micrometers
    DIM1 DECIMAL(8,1) NOT NULL DEFAULT 0,
    DIM2 DECIMAL(8,1) NOT NULL DEFAULT 0,
    DIM3 DECIMAL(8,1) NOT NULL DEFAULT 0,
    PRIMARY KEY (ENT), 
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE,
    FOREIGN KEY (TTL) REFERENCES TTL(ENT) ON DELETE CASCADE
);

-- article / artifact
DROP TABLE IF EXISTS ART;
CREATE TABLE ART (
    OBJ BIGINT NOT NULL,
    WHAT BIGINT,
    CREA DATE not null default (CURRENT_DATE),
    LTE TINYINT(1) DEFAULT 0,
    VAL TINYINT(1) DEFAULT 0,
    PUB TINYINT(1) DEFAULT 0,
    PRIMARY KEY (OBJ),
    FOREIGN KEY (OBJ)  REFERENCES OBJ(ENT) ON DELETE CASCADE,
    FOREIGN KEY (WHAT) REFERENCES TTL(ENT) ON DELETE CASCADE
);

-- article / artifact
DROP TABLE IF EXISTS CON;
CREATE TABLE CON (
    OBJ BIGINT NOT NULL,
    PRIMARY KEY (OBJ),
    FOREIGN KEY (OBJ)  REFERENCES OBJ(ENT) ON DELETE CASCADE
);
-- ============================================================
-- ## person / institution / location / exhibition
-- ============================================================
-- person / institution
DROP TABLE IF EXISTS PER;
CREATE TABLE PER (
    ENT BIGINT NOT NULL,
    LABEL VARCHAR(64) NOT NULL,
    INFO  VARCHAR(128), 
    PRIMARY KEY (ENT),
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE,
);
-- location
DROP TABLE IF EXISTS LOC;
CREATE TABLE LOC (
    ENT BIGINT NOT NULL,
    LABEL VARCHAR(64) NOT NULL,
    INFO  VARCHAR(128), 
    PRIMARY KEY (ENT),
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE,
);
-- exhibition
DROP TABLE IF EXISTS EXH;
CREATE TABLE EXH (
    ENT BIGINT NOT NULL,
    TTL BIGINT NOT NULL,
    BEG DATE not null default (CURRENT_DATE),
    END DATE not null default (CURRENT_DATE),
    PRIMARY KEY (ENT),
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE,
    FOREIGN KEY (TTL) REFERENCES TTL(ENT) ON DELETE CASCADE
);

-- person / institution - location
-- exhibition - location
-- via entity key
DROP TABLE IF EXISTS ENT_LOC;
CREATE TABLE ENT_LOC (
    ENT BIGINT NOT NULL,
    LOC BIGINT NOT NULL,
    -- primary location
    PRI TINYINT(1) DEFAULT 0,
    PRIMARY KEY (ENT, LOC),
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE,
    FOREIGN KEY (LOC) REFERENCES LOC(ENT) ON DELETE CASCADE
);

-- exhibition - person / institution
DROP TABLE IF EXISTS EXH_PER;
CREATE TABLE EXH_PER (
    EXH BIGINT NOT NULL,
    PER BIGINT NOT NULL,
    ORD INT DEFAULT 0,
    PRIMARY KEY (EXH, PER),
    FOREIGN KEY (EXH) REFERENCES EXH(ENT) ON DELETE CASCADE,
    FOREIGN KEY (PER) REFERENCES PER(ENT) ON DELETE CASCADE
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
DROP TABLE IF EXISTS OBJ_IMG;
CREATE TABLE OBJ_IMG (
    OBJ BIGINT NOT NULL,
    IMG BIGINT NOT NULL,
    ORD INT NOT NULL DEFAULT 1,
    PRIMARY KEY (OBJ, IMG),
    FOREIGN KEY (OBJ) REFERENCES OBJ(ENT) ON DELETE CASCADE,
    FOREIGN KEY (IMG) REFERENCES IMG(ID) ON DELETE CASCADE
);
-- ============================================================
-- ## sequences
-- ============================================================
DROP TABLE IF EXISTS SEQ;
CREATE TABLE SEQ (  
    ID TINYINT NOT NULL,
    NUM BIGINT NOT NULL,
    PRIMARY KEY (ID)
);
INSERT INTO SEQ VALUES(1, 0);
-- ============================================================
-- ## users
-- ============================================================
DROP TABLE IF EXISTS ROLE;
CREATE TABLE ROLE (  -- ROOT
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

drop table if exists USR_ENT;
create table USR_ENT (
    USR BIGINT not null,
    ENT BIGINT not null,
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    primary key (ENT, USR),
    foreign key (USR)  references USR(ID) on delete cascade,
    foreign key (ENT)  references ENT(ID) on delete cascade
);


-- ============================================================
-- ## Assigned Database Users
-- ============================================================
DELIMITER ;

DROP USER IF EXISTS 'aut'@'%';
CREATE USER 'aut'@'%' IDENTIFIED BY 'aa';
grant select on jagoda.* to 'aut'@'%';

-- GENERATED GRANT>
grant select                         on jagoda.LANG                 to 'aut'@'%';
grant select                         on jagoda.TTL_TYPE       to 'aut'@'%';
grant select, insert, delete         on jagoda.TTL            to 'aut'@'%';
grant select, insert, delete         on jagoda.TTL_ELEM            to 'aut'@'%';
grant select, insert, delete         on jagoda.OBJ                  to 'aut'@'%';
grant select, insert, delete         on jagoda.ART                  to 'aut'@'%';
grant select, insert, delete         on jagoda.OBJ_REC              to 'aut'@'%';
grant select, insert, delete         on jagoda.IMG                  to 'aut'@'%';
grant select, insert, delete         on jagoda.OBJ_IMG              to 'aut'@'%';
grant select, insert, delete         on jagoda.SEQ                  to 'aut'@'%';
grant select                         on jagoda.ROLE                 to 'aut'@'%';
grant select, insert, delete         on jagoda.USR                  to 'aut'@'%';
grant update (STD, TST                                ) on jagoda.TTL            to 'aut'@'%';
grant update (LABEL                                   ) on jagoda.TTL_ELEM            to 'aut'@'%';
grant update (TTL, DIM1, DIM2, DIM3, LOC, TST         ) on jagoda.OBJ                  to 'aut'@'%';
grant update (WHAT, YEAR, CNT, VAL, PUB               ) on jagoda.ART                  to 'aut'@'%';
grant update (TST                                     ) on jagoda.OBJ_REC              to 'aut'@'%';
grant update (ORD                                     ) on jagoda.OBJ_IMG              to 'aut'@'%';
grant update (NUM                                     ) on jagoda.SEQ                  to 'aut'@'%';
grant update (NAME, PASS, RC                          ) on jagoda.USR                  to 'aut'@'%';
-- <GENERATED GRANT

