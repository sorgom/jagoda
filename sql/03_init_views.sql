-- ============================================================
-- ### VIEWS
--  dependencies:
--      - init_functions
-- ============================================================

-- views to create
--  - all unused langage items
--  - all objects without image

-- all objects with 1st image
drop view if exists OBJ_IMG_1ST;
create view OBJ_IMG_1ST as
select T1.OBJ, imgFileMini(T1.IMG) as SRC from OBJ_IMG as T1
inner join
(select OBJ, min(ORD) as MINORD from OBJ_IMG group by OBJ) as T2
ON T1.OBJ = T2.OBJ AND T1.ORD = T2.MINORD;

--  all objects with assigend or default image
drop view if exists OBJ_IMG_DEF;
create view OBJ_IMG_DEF as
select T1.ID as OBJ, coalesce(T2.SRC, imgFileMini(0)) as SRC 
from OBJ as T1
left join OBJ_IMG_1ST as T2
on T1.ID = T2.OBJ
;

--  unused images
drop view if exists UNUSED_IMGS;
create view UNUSED_IMGS as
SELECT T1.ID, imgFileMini(T1.ID) as SRC, -1 as ORD FROM IMG AS T1
LEFT JOIN  OBJ_IMG AS T2 
ON T2.IMG = T1.ID
WHERE T2.IMG IS NULL
ORDER BY T1.ID;

-- title can be / is standard
drop view if exists TTL_INFO;
create view TTL_INFO as
select T1.*, T2.STDABLE
from TTL as T1
inner join TTP as T2
on T1.TPC = T2.TPC;

-- all assigned title elements with order
drop view if exists TTL_ORD;
create view TTL_ORD as
select T1.*, T2.ORD, T3.*
from TTL_ELEM as T1
inner join LANG as T2
on T1.ILC = T2.ILC
inner join TTL_INFO as T3
on T1.TTL = T3.ID
;

-- first available title
drop view if exists TTL_1ST;
create view TTL_1ST as
select T1.* from TTL_ORD as T1
inner join (select TTL, min(ORD) as MINORD from TTL_ORD group by TTL) as T2
on T1.TTL = T2.TTL and T1.ORD = T2.MINORD
;

drop view if exists TTL_X;
create view TTL_X as
select T1.*, getLabel(T2.LABEL, T3.ILC, T3.LABEL) as LABEL
from
(
    select T2.ID as TTL, T1.ILC
    from LANG as T1
    cross join TTL as T2
) as T1
left join TTL_ELEM as T2
on T2.TTL = T1.TTL and T2.ILC = T1.ILC
left join TTL_1ST as T3
on T3.TTL = T1.TTL
;

drop view if exists OBJ_TTL_INFO;
create view OBJ_TTL_INFO as
select T1.ID as OBJ, T2.ID as TTL, T2.STD, T2.STDABLE
from OBJ as T1
inner join TTL_INFO as T2
on T2.ID = T1.TTL
;

-- caption elements
drop view if exists CAP_ORD;
create view CAP_ORD as
select T1.*, T2.ORD
from CAP_ELEM as T1
inner join LANG as T2
on T1.ILC = T2.ILC
;

-- first available captions
drop view if exists CAP_1ST;
create view CAP_1ST as
select T1.* from CAP_ORD as T1
inner join (select CAP, min(ORD) as MINORD from CAP_ORD group by CAP) as T2
on T1.CAP = T2.CAP and T1.ORD = T2.MINORD
;

-- GENERATED GRANT>
grant select on jagoda.OBJ_IMG_1ST  to 'aut'@'%';
grant select on jagoda.OBJ_IMG_DEF  to 'aut'@'%';
grant select on jagoda.UNUSED_IMGS  to 'aut'@'%';
grant select on jagoda.TTL_INFO     to 'aut'@'%';
grant select on jagoda.TTL_ORD      to 'aut'@'%';
grant select on jagoda.TTL_1ST      to 'aut'@'%';
grant select on jagoda.TTL_X        to 'aut'@'%';
grant select on jagoda.OBJ_TTL_INFO to 'aut'@'%';
grant select on jagoda.CAP_ORD      to 'aut'@'%';
grant select on jagoda.CAP_1ST      to 'aut'@'%';
-- <GENERATED GRANT