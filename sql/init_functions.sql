-- ============================================================
-- ### PROCEDURES & FUNCTIONS
-- ============================================================
-- enables funtions / procedures that don't acces any tables:
SET GLOBAL log_bin_trust_function_creators = 1;
-- ============================================================
-- GENERATED>
DROP FUNCTION  IF EXISTS nextId;
DROP PROCEDURE IF EXISTS initSeq;
DROP PROCEDURE IF EXISTS getLangTable;
DROP PROCEDURE IF EXISTS getLangItemTypeTable;
DROP PROCEDURE IF EXISTS getLangItemTypeLabel;
DROP PROCEDURE IF EXISTS getLangItemType;
DROP PROCEDURE IF EXISTS newLangItem;
DROP PROCEDURE IF EXISTS getLangElemTable;
DROP PROCEDURE IF EXISTS getLangElem;
DROP PROCEDURE IF EXISTS setLangElem;
DROP FUNCTION  IF EXISTS isObject;
DROP FUNCTION  IF EXISTS imgPath;
DROP FUNCTION  IF EXISTS imgFileMini;
DROP FUNCTION  IF EXISTS imgFileFull;
DROP FUNCTION  IF EXISTS imgFileExif;
DROP PROCEDURE IF EXISTS imgFiles;
DROP PROCEDURE IF EXISTS imgFolders;
DROP PROCEDURE IF EXISTS addImg;
DROP PROCEDURE IF EXISTS addObjectImg;
DROP PROCEDURE IF EXISTS getObjectImgs;
DROP PROCEDURE IF EXISTS setObjectImg;
DROP PROCEDURE IF EXISTS rmObjectImg;
DROP PROCEDURE IF EXISTS getUnusedImgs;
DROP PROCEDURE IF EXISTS setUsr;
DROP FUNCTION  IF EXISTS getUsrId;
DROP PROCEDURE IF EXISTS setPass;
-- <GENERATED
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
    SELECT COUNT(*) FROM OBJECT WHERE (ID = pID) INTO @vNUM;  
    RETURN @vNUM;
END :)  
-- ============================================================
-- images
-- ============================================================
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
-- retrieve all unassigned images
CREATE PROCEDURE getUnusedImgs()
BEGIN
    SELECT I.ID, imgFileMini(I.ID) FROM IMG AS I
    LEFT JOIN  OBJECT_IMG AS OI 
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
-- GENERATED>
GRANT EXECUTE ON FUNCTION  jagoda.nextId                 TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.initSeq                TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangTable           TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangItemTypeTable   TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangItemTypeLabel   TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangItemType        TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.newLangItem            TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangElemTable       TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getLangElem            TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.setLangElem            TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION  jagoda.isObject               TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION  jagoda.imgPath                TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION  jagoda.imgFileMini            TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION  jagoda.imgFileFull            TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION  jagoda.imgFileExif            TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.imgFiles               TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.imgFolders             TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.addImg                 TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.addObjectImg           TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getObjectImgs          TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.setObjectImg           TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.rmObjectImg            TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.getUnusedImgs          TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.setUsr                 TO 'aut'@'%';
GRANT EXECUTE ON FUNCTION  jagoda.getUsrId               TO 'aut'@'%';
GRANT EXECUTE ON PROCEDURE jagoda.setPass                TO 'aut'@'%';
-- <GENERATED
