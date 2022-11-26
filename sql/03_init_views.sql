-- ============================================================
-- ### VIEWS
--  dependencies:
--      - init_functions
-- ============================================================

-- views to create
--  - all unused langage items
--  - all objects without image

-- all objects with 1st image
drop view if exists ENT_IMG_1ST;
create view ENT_IMG_1ST as
select T1.OBJ as ID, imgFileMini(T1.IMG) as SRC from ENT_IMG as T1
inner join
(select OBJ, min(ORD) as ORD2 from ENT_IMG group by OBJ) as T2
ON T1.OBJ = T2.OBJ AND T1.ORD = T2.ORD2;

--  all objects with assigend or default image
drop view if exists ENT_IMG_DEF;
create view ENT_IMG_DEF as
select T1.*, coalesce(T2.SRC, imgFileMini(0)) as SRC from OBJ as T1
left join
ENT_IMG_1ST as T2
on T1.ID = T2.ID
;

-- language item can be / is standard
drop view if exists TTL_STD;
create view TTL_STD as
select LI.*, LT.STDABLE
from 
TTL as LI
inner join TTL_TYPE as LT
on LI.TPC = LT.TPC;

-- all assigned language elements with order
drop view if exists TTL_ELEM_ORD;
create view TTL_ELEM_ORD as
select LE.ID, LE.LABEL, LA.ILC, LA.ORD from TTL_ELEM as LE
inner join LANG as LA
on LA.ILC = LE.ILC
order by LE.ID, LA.ORD;

-- first available language element
drop view if exists TTL_1ST;
create view TTL_1ST as
select LI.*, LE.LABEL, LE.ILC from TTL_ELEM_ORD as LE
inner join (select ID, min(ORD) as MIO from TTL_ELEM_ORD group by ID) as MO
on LE.ID = MO.ID and LE.ORD = MO.MIO
inner join TTL_STD as LI
on LI.ID = LE.ID; 
-- order by LI.TST desc, LE.ID;

--  all objects with (default or first) image and label
drop view if exists ENT_IMG_LABEL;
create view ENT_IMG_LABEL as
select T1.*, T2.LABEL, T2.STD, T2.STDABLE
from ENT_IMG_DEF as T1
inner join TTL_1ST as T2
on T1.TTL = T2.ID
;

--  all articles with (default or first) image and label
drop view if exists ART_FULL;
create view ART_FULL as
select T1.*, T2.*, coalesce(T3.LABEL, '??') as WLABEL from ART as T1
inner join ENT_IMG_LABEL as T2
on T1.OBJ = T2.ID
left join TTL_1ST as T3
on T1.WHAT = T3.ID
;

-- cross table all elements all languages
-- pre-filled with what's available
drop view if exists TTL_ELEM_X;
create view TTL_ELEM_X as
select LX.ID, LX.ILC, coalesce(LEO.LABEL, LE1.LABEL) as LABEL from 
(
    select LI.ID, LA.ILC from TTL as LI
    join
    LANG as LA
) as LX
inner join
TTL_1ST as LE1
on  LX.ID = LE1.ID
left join
TTL_ELEM_ORD as LEO
on
LX.ID = LEO.ID and
LX.ILC = LEO.ILC
order by LX.ID
;

-- select ID, SRC, LABEL, TST from ART_IMG_LABEL
-- order by TST desc
-- limit 20
-- ; 