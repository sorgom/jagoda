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
select T1.OBJ as ID, imgFileMini(T1.IMG) as SRC from OBJ_IMG as T1
inner join
(select OBJ, min(ORD) as ORD2 from OBJ_IMG group by OBJ) as T2
ON T1.OBJ = T2.OBJ AND T1.ORD = T2.ORD2;

-- language item can be / is standard
drop view if exists LANG_ITEM_STD;
create view LANG_ITEM_STD as
select LI.*, LT.STDABLE
from 
LANG_ITEM as LI
inner join LANG_ITEM_TYPE as LT
on LI.TPC = LT.TPC;

-- all assigned language elements with order
drop view if exists LANG_ELEM_ORD;
create view LANG_ELEM_ORD as
select LE.ID, LE.LABEL, LA.ILC, LA.ORD from LANG_ELEM as LE
inner join
LANG as LA
on LA.ILC = LE.ILC
order by LE.ID, LA.ORD;

-- first available language element
drop view if exists LANG_ELEM_1ST;
create view LANG_ELEM_1ST as
select LE.ID, LE.LABEL, LE.ILC, LI.STD, LI.TPC from LANG_ELEM_ORD as LE
inner join (select ID, min(ORD) as MIO from LANG_ELEM_ORD group by ID) as MO
on LE.ID = MO.ID and LE.ORD = MO.MIO
inner join LANG_ITEM as LI
on LI.ID = LE.ID 
order by LE.ID;

-- cross table all elements all languages
-- pre-filled with what's available
drop view if exists LANG_ELEM_X;
create view LANG_ELEM_X as
select LX.ID, LX.ILC, coalesce(LEO.LABEL, LE1.LABEL) as LABEL from 
(
    select LI.ID, LA.ILC from LANG_ITEM as LI
    join
    LANG as LA
) as LX
inner join
LANG_ELEM_1ST as LE1
on  LX.ID = LE1.ID
left join
LANG_ELEM_ORD as LEO
on
LX.ID = LEO.ID and
LX.ILC = LEO.ILC
order by LX.ID
;

