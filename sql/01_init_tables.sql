-- ============================================================
-- ### TABLES
-- ============================================================
-- Database collation: utf8mb4_bin
drop Database if exists jagoda;
create Database jagoda collate utf8mb4_bin;
use jagoda;

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';
-- ============================================================
-- ## language support
-- ============================================================

-- language definitions
-- ILC, ISO Language Codes acc. to 
-- https://www.w3schools.com/tags/ref_language_codes.asp
DROP TABLE IF EXISTS LANG;
CREATE TABLE LANG ( -- ROOT
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(64) NOT NULL,
    ORD INT NOT NULL,
    PUB TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (ILC),
    UNIQUE(ORD)
) ENGINE=INNODB;

-- title type
DROP TABLE IF EXISTS TTP;
CREATE TABLE TTP ( -- ROOT
    TPC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    STDABLE TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (TPC)
) ENGINE=INNODB;

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
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    PRIMARY KEY (ID),
    FOREIGN KEY (TPC) REFERENCES TTP(TPC) ON DELETE CASCADE,
    index(TPC),
    index(TST)
) ENGINE=INNODB;

-- TTL element for all languages
DROP TABLE IF EXISTS TTL_ELEM;
CREATE TABLE TTL_ELEM (
    TTL BIGINT NOT NULL, -- FIX
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    PRIMARY KEY (TTL, ILC),
    FOREIGN KEY (TTL) REFERENCES TTL(ID) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE,
    index(TTL),
    index(ILC)
) ENGINE=INNODB;

-- long text descriptions
DROP TABLE IF EXISTS TXT;
CREATE TABLE TXT (
    ID BIGINT NOT NULL,
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    PRIMARY KEY (ID),
    index(TST)
) ENGINE=INNODB;

-- TXT element for all languages
DROP TABLE IF EXISTS TXT_ELEM;
CREATE TABLE TXT_ELEM (
    TXT BIGINT NOT NULL, -- FIX
    ILC CHAR(2) NOT NULL,
    CONT LONGTEXT,
    PRIMARY KEY (TXT, ILC),
    FOREIGN KEY (TXT) REFERENCES TXT(ID) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE,
    index(TXT),
    index(ILC)
) ENGINE=INNODB;

-- website captions
DROP TABLE IF EXISTS CAP;
CREATE TABLE CAP (
    ID BIGINT NOT NULL,
    CPC VARCHAR(16) NOT NULL, -- FIX
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    PRIMARY KEY (ID),
    index(CPC),
    index(TST)
) ENGINE=INNODB;

-- CAP element for all languages
DROP TABLE IF EXISTS CAP_ELEM;
CREATE TABLE CAP_ELEM (
    CAP BIGINT NOT NULL,
    ILC CHAR(2) NOT NULL,
    LABEL VARCHAR(128) NOT NULL,
    PRIMARY KEY (CAP, ILC),
    FOREIGN KEY (CAP) REFERENCES CAP(ID) ON DELETE CASCADE,
    FOREIGN KEY (ILC) REFERENCES LANG(ILC) ON DELETE CASCADE,
    index(CAP),
    index(ILC)
) ENGINE=INNODB;

-- ============================================================
-- ## content elements
-- ============================================================
-- physical objects
DROP TABLE IF EXISTS OBJ;
CREATE TABLE OBJ (
    ID BIGINT NOT NULL,
    TTL BIGINT NOT NULL,
    NRD TINYINT(1) NOT NULL DEFAULT 0,
    DIM1 DECIMAL(8,1) NOT NULL DEFAULT 0,
    DIM2 DECIMAL(8,1) NOT NULL DEFAULT 0,
    DIM3 DECIMAL(8,1) NOT NULL DEFAULT 0,
    WHAT BIGINT,
    YEAR INT not null default 1900,
    VAL TINYINT(1) DEFAULT 0,
    PUB TINYINT(1) DEFAULT 0,
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    PRIMARY KEY (ID), 
    FOREIGN KEY (TTL) REFERENCES TTL(ID) ON DELETE CASCADE,
    FOREIGN KEY (WHAT) REFERENCES TTL(ID) ON DELETE CASCADE,
    index(TTL),
    index(WHAT),
    index(YEAR),
    index(TST)
) ENGINE=INNODB;

-- ============================================================
-- ## object grouping
-- ============================================================
DROP TABLE IF EXISTS GRP;
CREATE TABLE GRP (
    ID BIGINT NOT NULL,
    TTL BIGINT NOT NULL,
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    PRIMARY KEY (ID), 
    FOREIGN KEY (TTL) REFERENCES TTL(ID) ON DELETE CASCADE,
    index(TTL),
    index(TST)
) ENGINE=INNODB;

DROP TABLE IF EXISTS GRP_OBJ;
CREATE TABLE GRP_OBJ (
    GRP BIGINT NOT NULL,
    OBJ BIGINT NOT NULL,
    PRIMARY KEY (GRP, OBJ), 
    FOREIGN KEY (GRP) REFERENCES GRP(ID) ON DELETE CASCADE,
    FOREIGN KEY (OBJ) REFERENCES OBJ(ID) ON DELETE CASCADE,
    index(GRP),
    index(OBJ)
) ENGINE=INNODB;

-- 
-- ============================================================
-- ## images
-- ============================================================
--  list of existing images
DROP TABLE IF EXISTS IMG;
CREATE TABLE IMG (
    ID BIGINT NOT NULL,
    PRIMARY KEY (ID)
) ENGINE=INNODB;

-- object image assignment
DROP TABLE IF EXISTS OBJ_IMG;
CREATE TABLE OBJ_IMG (
    OBJ BIGINT NOT NULL,
    IMG BIGINT NOT NULL,
    ORD INT NOT NULL DEFAULT 0,
    PRIMARY KEY (OBJ, IMG),
    FOREIGN KEY (OBJ) REFERENCES OBJ(ID) ON DELETE CASCADE,
    FOREIGN KEY (IMG) REFERENCES IMG(ID) ON DELETE CASCADE,
    index(OBJ),
    index(IMG),
    index(ORD)
) ENGINE=INNODB;
-- ============================================================
-- ## sequences
-- ============================================================
DROP TABLE IF EXISTS SEQ;
CREATE TABLE SEQ (  
    ID TINYINT NOT NULL,
    NUM BIGINT NOT NULL,
    PRIMARY KEY (ID)
) ENGINE=INNODB;
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
    FOREIGN KEY (RC) REFERENCES ROLE(RC) ON DELETE CASCADE,
    UNIQUE(NAME) 
) CHARACTER SET latin1;

drop table if exists USR_OBJ;
create table USR_OBJ (
    USR BIGINT not null,
    OBJ BIGINT not null,
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    primary key (OBJ, USR),
    foreign key (USR)  references USR(ID) on delete cascade,
    foreign key (OBJ)  references OBJ(ID) on delete cascade,
    index(OBJ),
    index(USR),
    index(TST)
) ENGINE=INNODB;

drop table if exists USR_TTL;
create table USR_TTL (
    USR BIGINT not null,
    TTL BIGINT not null,
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    primary key (TTL, USR),
    foreign key (USR)  references USR(ID) on delete cascade,
    foreign key (TTL)  references TTL(ID) on delete cascade,
    index(TTL),
    index(USR),
    index(TST)
) ENGINE=INNODB;

-- ============================================================
-- ## Assigned Database Users
-- ============================================================
DELIMITER ;
SET foreign_key_checks = 1;

DROP USER IF EXISTS 'aut'@'%';
CREATE USER 'aut'@'%' IDENTIFIED BY 'aa';
grant select on jagoda.* to 'aut'@'%';

-- GENERATED GRANT>
grant select                         on jagoda.LANG                 to 'aut'@'%';
grant select                         on jagoda.TTP                  to 'aut'@'%';
grant select, insert, delete         on jagoda.TTL                  to 'aut'@'%';
grant select, insert, delete         on jagoda.TTL_ELEM             to 'aut'@'%';
grant select, insert, delete         on jagoda.TXT                  to 'aut'@'%';
grant select, insert, delete         on jagoda.TXT_ELEM             to 'aut'@'%';
grant select, insert, delete         on jagoda.CAP                  to 'aut'@'%';
grant select, insert, delete         on jagoda.CAP_ELEM             to 'aut'@'%';
grant select, insert, delete         on jagoda.OBJ                  to 'aut'@'%';
grant select, insert, delete         on jagoda.GRP                  to 'aut'@'%';
grant select, insert, delete         on jagoda.GRP_OBJ              to 'aut'@'%';
grant select, insert, delete         on jagoda.IMG                  to 'aut'@'%';
grant select, insert, delete         on jagoda.OBJ_IMG              to 'aut'@'%';
grant select, insert, delete         on jagoda.SEQ                  to 'aut'@'%';
grant select                         on jagoda.ROLE                 to 'aut'@'%';
grant select, insert, delete         on jagoda.USR                  to 'aut'@'%';
grant select, insert, delete         on jagoda.USR_OBJ              to 'aut'@'%';
grant select, insert, delete         on jagoda.USR_TTL              to 'aut'@'%';
grant update (LABEL, ORD, PUB                         ) on jagoda.LANG                 to 'aut'@'%';
grant update (LABEL                                   ) on jagoda.TTP                  to 'aut'@'%';
grant update (STD, TST                                ) on jagoda.TTL                  to 'aut'@'%';
grant update (LABEL                                   ) on jagoda.TTL_ELEM             to 'aut'@'%';
grant update (TST                                     ) on jagoda.TXT                  to 'aut'@'%';
grant update (CONT                                    ) on jagoda.TXT_ELEM             to 'aut'@'%';
grant update (TST                                     ) on jagoda.CAP                  to 'aut'@'%';
grant update (CAP, LABEL                              ) on jagoda.CAP_ELEM             to 'aut'@'%';
grant update (TTL, NRD, DIM1, DIM2, DIM3, WHAT, YEAR, VAL, PUB, TST) on jagoda.OBJ                  to 'aut'@'%';
grant update (TTL, TST                                ) on jagoda.GRP                  to 'aut'@'%';
grant update (GRP                                     ) on jagoda.GRP_OBJ              to 'aut'@'%';
grant update (ORD                                     ) on jagoda.OBJ_IMG              to 'aut'@'%';
grant update (NUM                                     ) on jagoda.SEQ                  to 'aut'@'%';
grant update (RC, LABEL                               ) on jagoda.ROLE                 to 'aut'@'%';
grant update (NAME, PASS, RC                          ) on jagoda.USR                  to 'aut'@'%';
grant update (TST                                     ) on jagoda.USR_OBJ              to 'aut'@'%';
grant update (TTL, TST                                ) on jagoda.USR_TTL              to 'aut'@'%';
-- <GENERATED GRANT

