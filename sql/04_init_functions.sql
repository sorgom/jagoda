-- ============================================================
-- ### PROCEDURES & FUNCTIONS
-- ============================================================
-- enables funtions / procedures that don't acces any tables:
SET GLOBAL log_bin_trust_function_creators = 1;
-- ============================================================
-- GENERATED DROP>
drop function  if exists nextId;
drop procedure if exists initSeq;
drop procedure if exists getTtls;
drop procedure if exists addTtl;
drop procedure if exists addObj;
drop procedure if exists setTtlStd;
drop procedure if exists setTtl;
drop procedure if exists getUsrArticles;
drop procedure if exists addEntImg;
drop procedure if exists getUnusedImgs;
drop procedure if exists setUsr;
drop function  if exists getUsrId;
drop procedure if exists test;
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
    -- entity
         IFNULL((SELECT MAX(ID) FROM ENT), 0),
    -- image
         IFNULL((SELECT MAX(ID) FROM IMG), 0)
    ) INTO @num;
    REPLACE INTO SEQ VALUES(1, @num);
END :)  
-- ============================================================
-- language support
-- ============================================================
-- retrieve all titles of a type 
CREATE PROCEDURE getTtls(pTPC CHAR(2))  
BEGIN
    SELECT T1.TTL as ID, T1.ILC, T2.LABEL 
    FROM TTL_ELEM_ORD as T1
        INNER JOIN TTL as T2
        ON T1.TTL = T2.ID
        inner join ENT as T3
        on  T3.ID = T2.ID
    WHERE T2.TPC = pTPC
    ORDER BY T3.TST desc, T1.ORD;
END :)

-- add new title
create procedure addTtl(pID bigint, pTPC CHAR(2))
BEGIN
    set autocommit = 1;
    insert into ENT(ID) values (pID);
    insert into TTL(ID, TPC) values (pID, pTPC);
END :)
-- add new object
create procedure addObj(pID bigint, pTTL bigint)
BEGIN
    set autocommit = 1;
    insert into ENT(ID) values (pID);
    commit;
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
create procedure getUsrArticles(pUSR BIGINT)
begin
    select ID, SRC, LABEL, WLABEL from ART_FULL
    inner join USR_ENT
    on USR_ENT.ENT = ART_FULL.ID and USR_ENT.USR = pUSR
    order by USR_ENT.TST desc
    limit 50;
end :)

-- ============================================================
-- images
-- ============================================================
-- create new objet image assignment
CREATE PROCEDURE addEntImg(pENT BIGINT, pIMG BIGINT)
BEGIN
    DECLARE vORD INT;

    REPLACE INTO IMG VALUES(pIMG); 
    
    SELECT MAX(ORD) FROM ENT_IMG
    WHERE ENT = pENT
    INTO @vORD;

    SET @vORD = IFNULL(@vORD, -1);
    SET @vORD = @vORD + 1;

    REPLACE INTO ENT_IMG VALUES (pENT, pIMG, @vORD);
END :)  
-- retrieve all unassigned images
CREATE PROCEDURE getUnusedImgs()
BEGIN
    SELECT T1.ID, imgFileMini(T1.ID) as SRC, -1 as ORD FROM IMG AS T1
    LEFT JOIN  ENT_IMG AS T2 
    ON T2.IMG = T1.ID
    WHERE T2.IMG IS NULL
    ORDER BY T1.ID;
END :)  
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
create procedure test()
begin
    select * from ENT;
end :)


-- ============================================================
-- ## Assigned Database Users
-- ============================================================
DELIMITER ;
-- GENERATED GRANT>
grant execute on function  jagoda.nextId                 to 'aut'@'%';
grant execute on procedure jagoda.initSeq                to 'aut'@'%';
grant execute on procedure jagoda.getTtls                to 'aut'@'%';
grant execute on procedure jagoda.addTtl                 to 'aut'@'%';
grant execute on procedure jagoda.addObj                 to 'aut'@'%';
grant execute on procedure jagoda.setTtlStd              to 'aut'@'%';
grant execute on procedure jagoda.setTtl                 to 'aut'@'%';
grant execute on procedure jagoda.getUsrArticles         to 'aut'@'%';
grant execute on procedure jagoda.addEntImg              to 'aut'@'%';
grant execute on procedure jagoda.getUnusedImgs          to 'aut'@'%';
grant execute on procedure jagoda.setUsr                 to 'aut'@'%';
grant execute on function  jagoda.getUsrId               to 'aut'@'%';
grant execute on procedure jagoda.test                   to 'aut'@'%';
-- <GENERATED GRANT

