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
drop procedure if exists setTtlStd;
drop procedure if exists getStdTtls;
drop procedure if exists getWhats;
drop function  if exists getTtlLabel;
drop procedure if exists getCapsPro;
drop procedure if exists getCaps;
drop procedure if exists getUsrObjs;
drop procedure if exists getObj;
drop procedure if exists getObjTtl;
drop procedure if exists getObjsByWhat;
drop procedure if exists getObjsNoWhat;
drop procedure if exists getObjWhats;
drop procedure if exists addObjImg;
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
         IFNULL((SELECT MAX(ID) FROM TTL), 0),
         IFNULL((SELECT MAX(ID) FROM CAP), 0),
         IFNULL((SELECT MAX(ID) FROM OBJ), 0),
         IFNULL((SELECT MAX(ID) FROM GRP), 0),
         IFNULL((SELECT MAX(ID) FROM IMG), 0)
    ) INTO @num;
    REPLACE INTO SEQ VALUES(1, @num);
END :)  
-- ============================================================
-- language support
-- ============================================================
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

-- set title standard
create procedure setTtlStd(pID bigint, pSTD tinyint)
BEGIN
    declare vOK TINYINT;
    select STDABLE from TTL_INFO where ID = pID into @vOK;
    if @vOK THEN
        UPDATE TTL set STD = pSTD where ID = pID;
    end if;
END :)

-- list of standard titles
create procedure getStdTtls(pILC CHAR(2))
begin
    select T1.ID, getLabel(T2.LABEL, T3.ILC, T3.LABEL) as LABEL
    from
    (
        select ID from TTL where STD = 1
        order by TST desc
    ) as T1

    left join TTL_ELEM as T2
    on T2.TTL = T1.ID and T2.ILC = pILC
    left join TTL_1ST as T3
    on T3.TTL = T1.ID
    ;
end :)

-- list of what
create procedure getWhats(pILC CHAR(2))
begin
    select T1.ID, getLabel(T2.LABEL, T3.ILC, T3.LABEL) as LABEL
    from
    (
        select ID from TTL where TPC = 'TQ'
    ) AS T1

    left join TTL_ELEM as T2
    on T2.TTL = T1.ID and T2.ILC = pILC
    left join TTL_1ST as T3
    on T3.TTL = T1.ID
    ;
end :)

-- label of given title
create function getTtlLabel(pID BIGINT, pILC CHAR(2))
returns VARCHAR(128)
begin
    declare vLABEL VARCHAR(128);
    select getLabel(T2.LABEL, T1.ILC, T1.LABEL)
    from (
        select TTL, ILC, LABEL from TTL_1ST
        where TTL = pID
        limit 1
    ) as T1
    left join TTL_ELEM as T2
    on T2.TTL = T1.TTL and T2.ILC = pILC
    into @vLABEL;
    return @vLABEL;
end :)
-- ============================================================
-- captions
-- ============================================================
-- all captions with available label for production
create procedure getCapsPro(pILC CHAR(2))
begin
    select T1.CPC, coalesce(T2.LABEL, defCap(T3.LABEL)) as LABEL
    from CAP as T1
    left join CAP_ELEM as T2
    on T2.CAP = T1.ID and T2.ILC = pILC
    left join CAP_1ST as T3
    on T3.CAP = T1.ID
    where T3.LABEL is not null
    ;
end :)

create procedure getCaps(pILC CHAR(2))
begin
    select T1.ID, T1.CPC, getLabel(T2.LABEL, T3.ILC, T3.LABEL) as LABEL
    from CAP as T1
    left join CAP_ELEM as T2
    on T2.CAP = T1.ID and T2.ILC = pILC
    left join CAP_1ST as T3
    on T3.CAP = T1.ID
    ;
end :)

-- ============================================================
-- objects
-- ============================================================

--  get last objects of user
create procedure getUsrObjs(pUSR BIGINT, pILC CHAR(2), pLimit INT)
begin
    select T1.ID, T1.SRC, T2.LABEL, coalesce(T3.LABEL, notFound()) as WLABEL
    from (
        select T2.ID, T2.TTL, T2.WHAT, T3.SRC
        from
        (
            select OBJ from USR_OBJ where USR = pUSR
            order by TST desc
            limit pLimit
        ) as T1

        inner join OBJ as T2
        on T2.ID = T1.OBJ

        inner join OBJ_IMG_DEF as T3
        on T3.OBJ = T1.OBJ
    ) as T1

    left join TTL_X as T2
    on T2.TTL = T1.TTL and T2.ILC = pILC

    left join TTL_X as T3
    on T1.WHAT is not NULL and T3.TTL = T1.WHAT and T3.ILC = pILC
    ;
end :)

-- select single object by id & language
create procedure getObj(pID BIGINT, pILC CHAR(2))
begin
    select T1.*,
        getLabel(T2.LABEL, T3.ILC, T3.LABEL) as LABEL, 
        T3.STD, T3.STDABLE,
        getLabel(T4.LABEL, T5.ILC, T5.LABEL) as WLABEL
    from (
        select T1.*, T2.SRC
        from
        (
            select * from OBJ where ID = pID
            limit 1
        ) as T1

        inner join OBJ_IMG_DEF as T2
        on T2.OBJ = T1.ID
    ) as T1

    left join TTL_ELEM as T2
    on T2.TTL = T1.TTL and T2.ILC = pILC
    left join TTL_1ST as T3
    on T3.TTL = T1.TTL

    left join TTL_ELEM as T4
    on T4.TTL = T1.WHAT and T4.ILC = pILC
    left join TTL_1ST as T5
    on T5.TTL = T1.WHAT
    ;
end :)

-- select single object title by id & language
create procedure getObjTtl(pID BIGINT, pILC CHAR(2))
begin
    select getLabel(T2.LABEL, T3.ILC, T3.LABEL) as LABEL
    from 
    (
        select TTL from OBJ
        where ID = pID
        limit 1
    ) as T1

    left join TTL_ELEM as T2
    on T2.TTL = T1.TTL and T2.ILC = pILC
    left join TTL_1ST as T3
    on T3.TTL = T1.TTL
    ;
end :)

--  get objects data by WHAT
create procedure getObjsByWhat(pILC CHAR(2), pWHAT BIGINT)
begin
    if pWHAT = 0 then
        call getObjsNoWhat(pILC);
    else
        select T1.ID, T1.SRC, T2.LABEL, coalesce(T3.LABEL, notFound()) as WLABEL
        from (
            select T1.*, T2.SRC from
            (
                select * from OBJ
                where WHAT = pWHAT
            ) as T1
            inner join OBJ_IMG_DEF as T2
            on T2.OBJ = T1.ID
        ) as T1

        left join TTL_X as T2
        on T2.TTL = T1.TTL and T2.ILC = pILC

        left join TTL_X as T3
        on T1.WHAT is not NULL and T3.TTL = T1.WHAT and T3.ILC = pILC
        ;
    end if;
end :)

--  get objects with undifined WHAT
create procedure getObjsNoWhat(pILC CHAR(2))
begin
    select T1.ID, T1.SRC, T2.LABEL, notFound() as WLABEL
    from (
        select T1.*, T2.SRC from
        (
            select * from OBJ
            where WHAT is NULL
        ) as T1
        inner join OBJ_IMG_DEF as T2
        on T2.OBJ = T1.ID
    ) as T1

    left join TTL_X as T2
    on T2.TTL = T1.TTL and T2.ILC = pILC
    ;
end :)

create procedure getObjWhats(pILC CHAR(2))
begin
    select coalesce(T1.WHAT, 0) as WHAT, coalesce(T2.LABEL, notFound()) as LABEL, T1.CNT
    from
    (
        select WHAT, count(*) as CNT
        from OBJ
        group by WHAT
    ) as T1
    
    left join TTL_X as T2
    on T2.TTL = T1.WHAT and T2.ILC = pILC
    order by T1.CNT desc
    ;
end :)

-- ============================================================
-- images
-- ============================================================
-- create new objet image assignment
CREATE PROCEDURE addObjImg(pOBJ BIGINT, pIMG BIGINT)
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
    SELECT ID FROM USR WHERE (NAME = LOWER(pNAME) AND PASS = pMD5) limit 1 INTO @vID; 
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
grant execute on procedure jagoda.setTtlStd              to 'aut'@'%';
grant execute on procedure jagoda.getStdTtls             to 'aut'@'%';
grant execute on procedure jagoda.getWhats               to 'aut'@'%';
grant execute on function  jagoda.getTtlLabel            to 'aut'@'%';
grant execute on procedure jagoda.getCapsPro             to 'aut'@'%';
grant execute on procedure jagoda.getCaps                to 'aut'@'%';
grant execute on procedure jagoda.getUsrObjs             to 'aut'@'%';
grant execute on procedure jagoda.getObj                 to 'aut'@'%';
grant execute on procedure jagoda.getObjTtl              to 'aut'@'%';
grant execute on procedure jagoda.getObjsByWhat          to 'aut'@'%';
grant execute on procedure jagoda.getObjsNoWhat          to 'aut'@'%';
grant execute on procedure jagoda.getObjWhats            to 'aut'@'%';
grant execute on procedure jagoda.addObjImg              to 'aut'@'%';
grant execute on procedure jagoda.setUsr                 to 'aut'@'%';
grant execute on function  jagoda.getUsrId               to 'aut'@'%';
-- <GENERATED GRANT

