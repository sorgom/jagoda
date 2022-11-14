-- ============================================================
-- ### PROCEDURES & FUNCTIONS
-- ============================================================
-- enables funtions / procedures that don't acces any tables:
SET GLOBAL log_bin_trust_function_creators = 1;
-- ============================================================
-- GENERATED DROP>
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
-- language table
CREATE PROCEDURE getLangTable()  
BEGIN
    SELECT ILC, LABEL FROM LANG ORDER BY ORD;
END :)  
-- retrieve language element types
CREATE PROCEDURE getLangItemTypeTable()
BEGIN
    SELECT * FROM LANG_ITEM_TYPE;
END :)  
-- retrieve language element type label
CREATE PROCEDURE getLangItemTypeLabel(pTP CHAR(2))  
BEGIN
    SELECT LABEL FROM LANG_ITEM_TYPE WHERE TPC = pTP LIMIT 1;
END :)  
-- retrieve type of a language item
CREATE PROCEDURE getLangItemType(pID BIGINT)  
BEGIN
    SELECT TPC FROM LANG_ITEM WHERE ID = pID LIMIT 1;
END :)  
-- create new language item
CREATE PROCEDURE newLangItem(pID BIGINT, pTP CHAR(2))  
BEGIN
    INSERT INTO LANG_ITEM VALUES (pID, pTP);
END :)  
-- retrieve all language elements of a type 
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
-- retrieve language element by ID
CREATE PROCEDURE getLangElem(pID BIGINT)  
BEGIN
    SELECT L.ILC, E.LABEL
    FROM LANG_ELEM as E INNER JOIN LANG as L 
    ON E.ILC = L.ILC 
    WHERE E.ID = pID
    ORDER BY L.ORD;
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
CREATE FUNCTION isObject(pID BIGINT)
RETURNS INT
BEGIN  
    DECLARE vNUM INT;  
    SELECT COUNT(*) FROM OBJ WHERE (ID = pID) INTO @vNUM;  
    RETURN @vNUM;
END :)  
-- ============================================================
-- images
-- ============================================================
-- create new image element
CREATE PROCEDURE addImg(pID BIGINT)
BEGIN
    REPLACE INTO IMG(ID) VALUES (pID);
END :)  
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
-- retrieve all images of an object
CREATE PROCEDURE getObjectImgs(pOBJ BIGINT)
BEGIN
    SELECT IMG as id, ORD, imgFileMini(IMG) as src FROM OBJ_IMG
    WHERE OBJ = pOBJ
    ORDER BY ORD;
END :)  
-- alter object image assignment
CREATE PROCEDURE setObjectImg(pOBJ BIGINT, pIMG BIGINT, pORD INT)
BEGIN
    REPLACE INTO OBJ_IMG VALUES (pOBJ, pIMG, pORD);
END :)  
-- remove image from object
CREATE PROCEDURE rmObjectImg(pOBJ BIGINT, pIMG BIGINT)
BEGIN
    DELETE FROM OBJ_IMG WHERE OBJ = pOBJ AND IMG = pIMG;
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
-- change password of author by ID
CREATE PROCEDURE setPass(pID BIGINT, pMD5 VARCHAR(32)) 
BEGIN
    UPDATE USR SET PASS = pMD5 WHERE ID = pID;
END :)  
-- ============================================================
-- ## Assigned Database Users
-- ============================================================
DELIMITER ;
-- GENERATED GRANT>
-- <GENERATED GRANT
