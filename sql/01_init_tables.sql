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
    PRIMARY KEY (ID)
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

-- title type
DROP TABLE IF EXISTS TTP;
CREATE TABLE TTP ( -- ROOT
    TPC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    STDABLE TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (TPC)
);
INSERT INTO TTP VALUES
    ('OT', 'Object Titles', 1),
    ('TQ', 'Kinds of Objects', 0),
    ('GT', 'General Titles', 0)
;

-- title / object caption
DROP TABLE IF EXISTS TTL;
CREATE TABLE TTL (
    ID BIGINT NOT NULL,
    TPC CHAR(2) NOT NULL,
    STD TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES ENT(ID) ON DELETE CASCADE,
    FOREIGN KEY (TPC) REFERENCES TTP(TPC) ON DELETE CASCADE
);

-- TTL element for all languages
DROP TABLE IF EXISTS TTL_ELEM;
CREATE TABLE TTL_ELEM (
    TTL BIGINT NOT NULL, -- FIX
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    PRIMARY KEY (TTL, ILC),
    FOREIGN KEY (TTL) REFERENCES TTL(ID) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE
);

-- long text descriptions
DROP TABLE IF EXISTS TXT;
CREATE TABLE TXT (
    ID BIGINT NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES ENT(ID) ON DELETE CASCADE
);

-- TXT element for all languages
DROP TABLE IF EXISTS TXT_ELEM;
CREATE TABLE TXT_ELEM (
    TXT BIGINT NOT NULL, -- FIX
    ILC CHAR(2) NOT NULL,
    CONT LONGTEXT,
    PRIMARY KEY (TXT, ILC),
    FOREIGN KEY (TXT) REFERENCES TXT(ID) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE
);

-- website captions
DROP TABLE IF EXISTS CAP;
CREATE TABLE CAP (
    ID BIGINT NOT NULL,
    CPC VARCHAR(16) NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES ENT(ID) ON DELETE CASCADE
);

-- CAP element for all languages
DROP TABLE IF EXISTS CAP_ELEM;
CREATE TABLE CAP_ELEM (
    CAP BIGINT NOT NULL,
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    PRIMARY KEY (CAP, ILC),
    FOREIGN KEY (CAP) REFERENCES CAP(ID) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE
);


-- ============================================================
-- ## content elements
-- ============================================================
-- physical objects
DROP TABLE IF EXISTS OBJ;
CREATE TABLE OBJ (
    ID BIGINT NOT NULL,
    TTL BIGINT NOT NULL,
    NRD TINYINT(1) NOT NULL DEFAULT 0, -- FIX
    -- dimensions in micrometers
    DIM1 DECIMAL(8,1) NOT NULL DEFAULT 0,
    DIM2 DECIMAL(8,1) NOT NULL DEFAULT 0,
    DIM3 DECIMAL(8,1) NOT NULL DEFAULT 0,
    PRIMARY KEY (ID), 
    FOREIGN KEY (ID) REFERENCES ENT(ID) ON DELETE CASCADE,
    FOREIGN KEY (TTL) REFERENCES TTL(ID) ON DELETE CASCADE
);

-- article / artifact
DROP TABLE IF EXISTS ART;
CREATE TABLE ART (
    OBJ BIGINT NOT NULL,
    WHAT BIGINT,
    CRDT DATE not null default (CURRENT_DATE),
    VAL TINYINT(1) DEFAULT 0,
    PUB TINYINT(1) DEFAULT 0,
    PRIMARY KEY (OBJ),
    FOREIGN KEY (OBJ)  REFERENCES OBJ(ID) ON DELETE CASCADE,
    FOREIGN KEY (WHAT) REFERENCES TTL(ID) ON DELETE CASCADE
);

-- article / artifact
DROP TABLE IF EXISTS CON;
CREATE TABLE CON (
    OBJ BIGINT NOT NULL,
    PRIMARY KEY (OBJ),
    FOREIGN KEY (OBJ) REFERENCES OBJ(ID) ON DELETE CASCADE
);
-- ============================================================
-- ## object grouping
-- ============================================================
DROP TABLE IF EXISTS GRP;
CREATE TABLE GRP (
    ID BIGINT NOT NULL,
    TTL BIGINT NOT NULL,
    PRIMARY KEY (ID), 
    FOREIGN KEY (ID) REFERENCES ENT(ID) ON DELETE CASCADE,
    FOREIGN KEY (TTL) REFERENCES TTL(ID) ON DELETE CASCADE
);

DROP TABLE IF EXISTS GRP_OBJ;
CREATE TABLE GRP_OBJ (
    GRP BIGINT NOT NULL,
    OBJ BIGINT NOT NULL,
    PRIMARY KEY (GRP, OBJ), 
    FOREIGN KEY (GRP) REFERENCES GRP(ID) ON DELETE CASCADE,
    FOREIGN KEY (OBJ) REFERENCES OBJ(ID) ON DELETE CASCADE
);

-- ============================================================
-- ## person / institution / location / exhibition
-- ============================================================
-- person / institution
DROP TABLE IF EXISTS PER;
CREATE TABLE PER (
    ID BIGINT NOT NULL,
    LABEL VARCHAR(64) NOT NULL,
    INFO  VARCHAR(128), 
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES ENT(ID) ON DELETE CASCADE
);
-- location
DROP TABLE IF EXISTS LOC;
CREATE TABLE LOC (
    ID BIGINT NOT NULL,
    LABEL VARCHAR(64) NOT NULL,
    INFO  VARCHAR(128), 
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES ENT(ID) ON DELETE CASCADE
);
-- exhibition
DROP TABLE IF EXISTS EXH;
CREATE TABLE EXH (
    ID BIGINT NOT NULL,
    TTL BIGINT NOT NULL,
    BEG DATE not null default (CURRENT_DATE),
    END DATE not null default (CURRENT_DATE),
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES ENT(ID) ON DELETE CASCADE,
    FOREIGN KEY (TTL) REFERENCES TTL(ID) ON DELETE CASCADE
);

-- person / institution - location
-- exhibition - location
-- via entity key
DROP TABLE IF EXISTS LOC_ENT;
CREATE TABLE LOC_ENT (
    LOC BIGINT NOT NULL,
    ENT BIGINT NOT NULL,
    -- primary location
    PRI TINYINT(1) DEFAULT 0,
    PRIMARY KEY (LOC, ENT),
    FOREIGN KEY (LOC) REFERENCES LOC(ID) ON DELETE CASCADE,
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE
);

-- object location with object count / numbers
DROP TABLE IF EXISTS LOC_OBJ;
CREATE TABLE LOC_OBJ (
    LOC BIGINT NOT NULL,
    OBJ BIGINT NOT NULL,
    -- count or numbers ranges of pieces
    PCS JSON NOT NULL,
    PRIMARY KEY (LOC, OBJ),
    FOREIGN KEY (LOC) REFERENCES LOC(ID) ON DELETE CASCADE,
    FOREIGN KEY (OBJ) REFERENCES OBJ(ID) ON DELETE CASCADE
);

-- authors of objects
DROP TABLE IF EXISTS AUT_OBJ;
CREATE TABLE AUT_OBJ (
    PER BIGINT NOT NULL,
    OBJ BIGINT NOT NULL,
    PRIMARY KEY (PER, OBJ),
    FOREIGN KEY (PER) REFERENCES PER(ID) ON DELETE CASCADE,
    FOREIGN KEY (OBJ) REFERENCES OBJ(ID) ON DELETE CASCADE
);

-- owners of objects
DROP TABLE IF EXISTS OWN_OBJ;
CREATE TABLE OWN_OBJ (
    PER BIGINT NOT NULL,
    OBJ BIGINT NOT NULL,
    -- count or numbers ranges of pieces
    PCS JSON NOT NULL,
    PRIMARY KEY (PER, OBJ),
    FOREIGN KEY (PER) REFERENCES PER(ID) ON DELETE CASCADE,
    FOREIGN KEY (OBJ) REFERENCES OBJ(ID) ON DELETE CASCADE
);

-- exhibition - person / institution
DROP TABLE IF EXISTS EXH_PER;
CREATE TABLE EXH_PER (
    EXH BIGINT NOT NULL,
    PER BIGINT NOT NULL,
    ORD INT DEFAULT 0,
    PRIMARY KEY (EXH, PER),
    FOREIGN KEY (EXH) REFERENCES EXH(ID) ON DELETE CASCADE,
    FOREIGN KEY (PER) REFERENCES PER(ID) ON DELETE CASCADE
);

DROP TABLE IF EXISTS EXH_OBJ;
CREATE TABLE EXH_OBJ (
    EXH BIGINT NOT NULL,
    OBJ BIGINT NOT NULL,
    PRIMARY KEY (EXH, OBJ),
    FOREIGN KEY (EXH) REFERENCES EXH(ID) ON DELETE CASCADE,
    FOREIGN KEY (OBJ) REFERENCES OBJ(ID) ON DELETE CASCADE
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
DROP TABLE IF EXISTS ENT_IMG;
CREATE TABLE ENT_IMG (
    ENT BIGINT NOT NULL,
    IMG BIGINT NOT NULL,
    ORD INT NOT NULL DEFAULT 1,
    PRIMARY KEY (ENT, IMG),
    FOREIGN KEY (ENT) REFERENCES ENT(ID) ON DELETE CASCADE,
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
SET foreign_key_checks = 1;

DROP USER IF EXISTS 'aut'@'%';
CREATE USER 'aut'@'%' IDENTIFIED BY 'aa';
grant select on jagoda.* to 'aut'@'%';

-- GENERATED GRANT>
grant select, insert, delete         on jagoda.ENT                  to 'aut'@'%';
grant select                         on jagoda.LANG                 to 'aut'@'%';
grant select                         on jagoda.TTP                  to 'aut'@'%';
grant select, insert, delete         on jagoda.TTL                  to 'aut'@'%';
grant select, insert, delete         on jagoda.TTL_ELEM             to 'aut'@'%';
grant select, insert, delete         on jagoda.TXT                  to 'aut'@'%';
grant select, insert, delete         on jagoda.TXT_ELEM             to 'aut'@'%';
grant select, insert, delete         on jagoda.CAP                  to 'aut'@'%';
grant select, insert, delete         on jagoda.CAP_ELEM             to 'aut'@'%';
grant select, insert, delete         on jagoda.OBJ                  to 'aut'@'%';
grant select, insert, delete         on jagoda.ART                  to 'aut'@'%';
grant select, insert, delete         on jagoda.CON                  to 'aut'@'%';
grant select, insert, delete         on jagoda.GRP                  to 'aut'@'%';
grant select, insert, delete         on jagoda.GRP_OBJ              to 'aut'@'%';
grant select, insert, delete         on jagoda.PER                  to 'aut'@'%';
grant select, insert, delete         on jagoda.LOC                  to 'aut'@'%';
grant select, insert, delete         on jagoda.EXH                  to 'aut'@'%';
grant select, insert, delete         on jagoda.LOC_ENT              to 'aut'@'%';
grant select, insert, delete         on jagoda.LOC_OBJ              to 'aut'@'%';
grant select, insert, delete         on jagoda.AUT_OBJ              to 'aut'@'%';
grant select, insert, delete         on jagoda.OWN_OBJ              to 'aut'@'%';
grant select, insert, delete         on jagoda.EXH_PER              to 'aut'@'%';
grant select, insert, delete         on jagoda.EXH_OBJ              to 'aut'@'%';
grant select, insert, delete         on jagoda.IMG                  to 'aut'@'%';
grant select, insert, delete         on jagoda.ENT_IMG              to 'aut'@'%';
grant select, insert, delete         on jagoda.SEQ                  to 'aut'@'%';
grant select                         on jagoda.ROLE                 to 'aut'@'%';
grant select, insert, delete         on jagoda.USR                  to 'aut'@'%';
grant select, insert, delete         on jagoda.USR_ENT              to 'aut'@'%';
grant update (TST                                     ) on jagoda.ENT                  to 'aut'@'%';
grant update (LABEL, ORD                              ) on jagoda.LANG                 to 'aut'@'%';
grant update (LABEL                                   ) on jagoda.TTP                  to 'aut'@'%';
grant update (STD                                     ) on jagoda.TTL                  to 'aut'@'%';
grant update (LABEL                                   ) on jagoda.TTL_ELEM             to 'aut'@'%';
grant update (CONT                                    ) on jagoda.TXT_ELEM             to 'aut'@'%';
grant update (CPC                                     ) on jagoda.CAP                  to 'aut'@'%';
grant update (CAP, LABEL                              ) on jagoda.CAP_ELEM             to 'aut'@'%';
grant update (TTL, DIM1, DIM2, DIM3                   ) on jagoda.OBJ                  to 'aut'@'%';
grant update (WHAT, CRDT, VAL, PUB                    ) on jagoda.ART                  to 'aut'@'%';
grant update (TTL                                     ) on jagoda.GRP                  to 'aut'@'%';
grant update (GRP                                     ) on jagoda.GRP_OBJ              to 'aut'@'%';
grant update (LABEL, INFO                             ) on jagoda.PER                  to 'aut'@'%';
grant update (LABEL, INFO                             ) on jagoda.LOC                  to 'aut'@'%';
grant update (TTL, BEG, END                           ) on jagoda.EXH                  to 'aut'@'%';
grant update (LOC, PRI                                ) on jagoda.LOC_ENT              to 'aut'@'%';
grant update (LOC, PCS                                ) on jagoda.LOC_OBJ              to 'aut'@'%';
grant update (PER                                     ) on jagoda.AUT_OBJ              to 'aut'@'%';
grant update (PER, PCS                                ) on jagoda.OWN_OBJ              to 'aut'@'%';
grant update (EXH, PER, ORD                           ) on jagoda.EXH_PER              to 'aut'@'%';
grant update (EXH                                     ) on jagoda.EXH_OBJ              to 'aut'@'%';
grant update (ORD                                     ) on jagoda.ENT_IMG              to 'aut'@'%';
grant update (NUM                                     ) on jagoda.SEQ                  to 'aut'@'%';
grant update (RC, LABEL                               ) on jagoda.ROLE                 to 'aut'@'%';
grant update (NAME, PASS, RC                          ) on jagoda.USR                  to 'aut'@'%';
grant update (TST                                     ) on jagoda.USR_ENT              to 'aut'@'%';
-- <GENERATED GRANT

