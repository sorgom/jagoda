-- ============================================================
-- ### VIEWS
--  dependencies:
--      - init_functions
-- ============================================================

-- views to create
--  - all unused langage items
--  - all objects without image

-- all objects with 1st image
drop view if exists OBJECT_IMG_1ST;
create view OBJECT_IMG_1ST as
select T1.OBJECT as ID, imgFileMini(T1.IMG) as SRC from OBJECT_IMG as T1
inner join
(select OBJECT, min(ORD) as ORD2 from OBJECT_IMG GROUP BY OBJECT) as T2
ON T1.OBJECT = T2.OBJECT AND T1.ORD = T2.ORD2;

-- all assigned language elenets with order
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
select LE.ID, LE.LABEL, LE.ILC from LANG_ELEM_ORD as LE
inner join
(select ID, min(ORD) as MIO from LANG_ELEM_ORD group by ID) as MO
on LE.ID = MO.ID and LE.ORD = MO.MIO 
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

