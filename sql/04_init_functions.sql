-- ============================================================
-- ### PROCEDURES & FUNCTIONS
-- ============================================================
-- enables funtions / procedures that don't acces any tables:
set global log_bin_trust_function_creators = 1;
set global autocommit = 1;
-- ============================================================
-- GENERATED DROP>
drop function  if exists nextId;
drop procedure if exists initSeq;
drop function  if exists defIlc;
drop procedure if exists addTtl;
drop procedure if exists addObj;
drop procedure if exists setTtlStd;
drop procedure if exists setTtl;
drop procedure if exists getUsrArticles;
drop procedure if exists addEntImg;
drop procedure if exists getArtFull;
drop procedure if exists setUsr;
drop function  if exists getUsrId;
-- <GENERATED DROP
-- sequences
-- ============================================================
DELIMITER :)  
-- retrieve next id sequence value:
CREATE FUNCTION nextId()
RETURNS BIGINT
BEGIN  
    DECLARE vNUM BIGINT;  
    SELECT NUM FROM SEQ WHERE (ID = 1) INTO @vNUM; 
    SET @vNUM = IFNULL(@vNUM, 0) + 1;
    REPLACE INTO SEQ VALUES(1, @vNUM);
    RETURN @vNUM;
END :)  
-- initialize sequences counters
CREATE PROCEDURE initSeq()  
BEGIN
    DECLARE num BIGINT;
    SELECT GREATEST(
         IFNULL((SELECT MAX(ID) FROM ENT), 0),
         IFNULL((SELECT MAX(ID) FROM IMG), 0)
    ) INTO @num;
    REPLACE INTO SEQ VALUES(1, @num);
END :)  
-- ============================================================
-- language support
-- ============================================================
-- retrieve all titles of a type 
-- CREATE PROCEDURE getTtls(pTPC CHAR(2))  
-- BEGIN
--     SELECT T1.TTL as ID, T1.ILC, T2.LABEL 
--     FROM TTL_ELEM_ORD as T1
--         INNER JOIN TTL as T2
--         ON T1.TTL = T2.ID
--         inner join ENT as T3
--         on  T3.ID = T2.ID
--     WHERE T2.TPC = pTPC
--     ORDER BY T3.TST desc, T1.ORD;
-- END :)
create function defIlc()
returns CHAR(2)
begin
    declare vILC CHAR(2);
    select T1.ILC from LANG as T1
    inner join (select min(ORD) as MO from LANG) as T2
    on T1.ORD = T2.MO limit 1 
    into @vILC;
    return @vILC;
end :)

-- add new title
create procedure addTtl(pID bigint, pTPC CHAR(2))
BEGIN
    insert into ENT(ID) values (pID);
    insert into TTL(ID, TPC) values (pID, pTPC);
END :)
-- add new object
create procedure addObj(pID bigint, pTTL bigint)
BEGIN
    insert into ENT(ID) values (pID);
    insert into OBJ(ID, TTL) values (pID, pTTL);
END :)

-- set title standard
create procedure setTtlStd(pID bigint, pSTD tinyint)
BEGIN
    declare vOK TINYINT;
    select STDABLE from TTL_INFO where ID = pID into @vOK;
    if @vOK THEN
        UPDATE TTL set STD = pSTD where ID = pID;
    end if;
END :)
-- set language element
CREATE PROCEDURE setTtl(
    pTTL BIGINT, 
    pILC CHAR(2), 
    pLABEL VARCHAR(128)) 
BEGIN
    IF pLABEL = '' THEN
        DELETE FROM TTL_ELEM WHERE TTL = pTTL AND ILC = pILC;
    ELSE
        REPLACE INTO TTL_ELEM VALUES (pTTL, pILC, pLABEL);
    END IF;
END :)  
-- -- ============================================================
-- -- objects
-- -- ============================================================
--  get last articles of user
create procedure getUsrArticles(pUSR BIGINT, pILC CHAR(2))
begin
    select TAO.ID, TAO.SRC, TL.LABEL, TW.LABEL as WLABEL
    from ( 
        select TE.*, TA.* 
        from (
            select * from USR_ENT where USR = pUSR order by TST desc
        ) as TE
        inner join
        (
            select T1.ID, T1.TTL, T1.WHAT, T2.SRC
            from ART_OBJ as T1
            inner join OBJ_IMG_DEF as T2
            on T1.OBJ = T2.OBJ

        ) as TA
    ) as TAO
    inner join TTL_X as TL
    on TL.ID = TAO.TTL and TL.ILC = pILC
    inner join TTL_X as TW
    on TW.ID = TAO.WHAT and TL.ILC = pILC
    ;
end :)
-- ============================================================
-- images
-- ============================================================
-- create new objet image assignment
CREATE PROCEDURE addEntImg(pEnt BIGINT, pIMG BIGINT)
BEGIN
    DECLARE vORD INT;

    REPLACE INTO IMG VALUES(pIMG); 
    
    SELECT MAX(ORD) FROM ENT_IMG
    WHERE ENT = pEnt
    INTO @vORD;

    SET @vORD = IFNULL(@vORD, -1);
    SET @vORD = @vORD + 1;

    REPLACE INTO ENT_IMG VALUES (pEnt, pIMG, @vORD);
END :)  
-- ============================================================
-- obect, language, image getters
-- ============================================================
-- complete article with labels and default image
create procedure getArtFull(pOBJ BIGINT, pILC CHAR(2))
begin
    select * from ART_X where ID = pOBJ and ILC = pILC limit 1;
end :)

-- ============================================================
-- authors / users
-- ============================================================
-- add / modify an Author
CREATE PROCEDURE setUsr(pNAME VARCHAR(32), pPASS VARCHAR(32))  
BEGIN
    REPLACE INTO USR (NAME, PASS) VALUES(LOWER(pNAME), MD5(pPASS));
END :)  
-- retrieve author ID by name and password (MD5):
CREATE FUNCTION getUsrId(pNAME VARCHAR(32), pMD5 VARCHAR(32))  
RETURNS BIGINT
BEGIN  
    DECLARE vID BIGINT;
    SET @vID = -1;  
    SELECT ID FROM USR WHERE (NAME = LOWER(pNAME) AND PASS = pMD5) INTO @vID; 
    RETURN @vID;
END :)  
-- ============================================================
-- TEST
-- ============================================================

-- ============================================================
-- ## Assigned Database Users
-- ============================================================
DELIMITER ;
-- GENERATED GRANT>
grant execute on function  jagoda.nextId                 to 'aut'@'%';
grant execute on procedure jagoda.initSeq                to 'aut'@'%';
grant execute on function  jagoda.defIlc                 to 'aut'@'%';
grant execute on procedure jagoda.addTtl                 to 'aut'@'%';
grant execute on procedure jagoda.addObj                 to 'aut'@'%';
grant execute on procedure jagoda.setTtlStd              to 'aut'@'%';
grant execute on procedure jagoda.setTtl                 to 'aut'@'%';
grant execute on procedure jagoda.getUsrArticles         to 'aut'@'%';
grant execute on procedure jagoda.addEntImg              to 'aut'@'%';
grant execute on procedure jagoda.getArtFull             to 'aut'@'%';
grant execute on procedure jagoda.setUsr                 to 'aut'@'%';
grant execute on function  jagoda.getUsrId               to 'aut'@'%';
-- <GENERATED GRANT

