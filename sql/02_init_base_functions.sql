-- ============================================================
-- ### PROCEDURES & FUNCTIONS: BASE
-- ============================================================
-- enables funtions / procedures that don't acces any tables:
SET GLOBAL log_bin_trust_function_creators = 1;
-- ============================================================
-- GENERATED DROP>
drop function  if exists imgPath;
drop function  if exists imgFileMini;
drop function  if exists imgFileFull;
drop function  if exists imgFileExif;
drop procedure if exists imgFiles;
drop procedure if exists imgFolders;
drop function  if exists notFound;
-- <GENERATED DROP
DELIMITER :)  
-- ============================================================
-- images
-- ============================================================
CREATE FUNCTION imgPath(pSUB VARCHAR(8), pID BIGINT, pEXT VARCHAR(4))
RETURNS VARCHAR(32)
BEGIN
    IF pID = -1 THEN 
        RETURN CONCAT('/static/img/',  pSUB);
    ELSE 
        RETURN CONCAT('/static/img/',  pSUB, '/', LPAD(pID, 7, 0), '.', pEXT);
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
create function notFound()
RETURNS CHAR(3)
BEGIN
    return '*?*';
END :)

DELIMITER ;
-- GENERATED GRANT>
grant execute on function  jagoda.imgPath                to 'aut'@'%';
grant execute on function  jagoda.imgFileMini            to 'aut'@'%';
grant execute on function  jagoda.imgFileFull            to 'aut'@'%';
grant execute on function  jagoda.imgFileExif            to 'aut'@'%';
grant execute on procedure jagoda.imgFiles               to 'aut'@'%';
grant execute on procedure jagoda.imgFolders             to 'aut'@'%';
grant execute on function  jagoda.notFound               to 'aut'@'%';
-- <GENERATED GRANT
