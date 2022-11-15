-- ============================================================
-- ### PROCEDURES & FUNCTIONS
-- ============================================================
-- enables funtions / procedures that don't acces any tables:
SET GLOBAL log_bin_trust_function_creators = 1;
-- ============================================================
-- GENERATED DROP>
drop function  if exists nextId;
drop procedure if exists initSeq;
drop procedure if exists getLangElemTable;
drop procedure if exists setLangItemStd;
drop procedure if exists setLangElem;
drop procedure if exists addObjectImg;
drop procedure if exists getUnusedImgs;
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
    -- OBJ.ID
         IFNULL((SELECT MAX(ID) FROM OBJ), 0),
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
-- ============================================================
-- language support
-- ============================================================
-- retrieve all language elements of a type 
CREATE PROCEDURE getLangElemTable(pTPC CHAR(2))  
BEGIN
    SELECT E.ID, E.ILC, E.LABEL 
    FROM LANG_ELEM_ORD as E
        INNER JOIN LANG_ITEM as I
        ON E.ID = I.ID 
    WHERE I.TPC = pTPC
    ORDER BY E.ID, E.ORD;
END :)  
-- set language item standard
create procedure setLangItemStd(pID bigint, pSTD tinyint)
BEGIN
    declare vOK TINYINT;
    select STDABLE from LANG_ITEM_STD where ID = pID into @vOK;
    if @vOK THEN
        UPDATE LANG_ITEM set STD = pSTD where ID = pID;
    end if;
END :)
-- set language element
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
-- ============================================================
-- objects
-- ============================================================
-- ============================================================
-- images
-- ============================================================
-- create new objet image assignment
CREATE PROCEDURE addObjectImg(pOBJ BIGINT, pIMG BIGINT)
BEGIN
    DECLARE vORD INT;

    REPLACE INTO IMG VALUES(pIMG); 
    
    SELECT MAX(ORD) FROM OBJ_IMG
    WHERE OBJ = pOBJ
    INTO @vORD;

    SET @vORD = IFNULL(@vORD, -1);
    SET @vORD = @vORD + 1;

    REPLACE INTO OBJ_IMG VALUES (pOBJ, pIMG, @vORD);
END :)  
-- retrieve all unassigned images
CREATE PROCEDURE getUnusedImgs()
BEGIN
    SELECT I.ID as id, imgFileMini(I.ID) as src, -1 as ord FROM IMG AS I
    LEFT JOIN  OBJ_IMG AS OI 
    ON OI.IMG = I.ID
    WHERE OI.IMG IS NULL
    ORDER BY I.ID;
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
-- ## Assigned Database Users
-- ============================================================
DELIMITER ;
-- GENERATED GRANT>
grant execute on function  jagoda.nextId                 to 'aut'@'%';
grant execute on procedure jagoda.initSeq                to 'aut'@'%';
grant execute on procedure jagoda.getLangElemTable       to 'aut'@'%';
grant execute on procedure jagoda.setLangItemStd         to 'aut'@'%';
grant execute on procedure jagoda.setLangElem            to 'aut'@'%';
grant execute on procedure jagoda.addObjectImg           to 'aut'@'%';
grant execute on procedure jagoda.getUnusedImgs          to 'aut'@'%';
grant execute on procedure jagoda.setUsr                 to 'aut'@'%';
grant execute on function  jagoda.getUsrId               to 'aut'@'%';
-- <GENERATED GRANT
