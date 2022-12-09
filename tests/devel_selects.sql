
-- T1 OBJ OBJ
-- T2 OBJ ID TTL ...
-- T3 TTL_ELEM_X -> TTL_X ID ILC LABEL
-- T4 TTL_INFO -> ID TPC STDABLE STD
-- T5 TTL_ELEM_X -> TTL_X ID ILC LABEL
-- T6 OBJ_IMG_DEF OBJ SRC

drop view if exists ART_X;
create view ART_X as
select T1.*, T2.*, T3.ILC, T3.LABEL, T4.STD, T4.STDABLE, T5.LABEL as WLABEL, T6.SRC
from OBJ as T1
inner join OBJ as T2
on T1.OBJ = T2.ID
right join TTL_X as T3
on T2.TTL = T3.ID
inner join TTL_INFO as T4
on T2.TTL = T4.ID
inner join TTL_X as T5
on T1.WHAT = T5.ID and T5.ILC = T3.ILC
inner join OBJ_IMG_DEF as T6
on T6.OBJ = T2.ID
order by T2.ID, T3.ILC
;

select T1.ILC from LANG as T1
inner join (select min(ORD) as MO from LANG) as T2
on T1.ORD = T2.MO
limit 1;

drop procedure if exists getUsrObjicles;
DELIMITER :)  

CREATE TEMPORARY VIEW LX as
select ID, LABEL
from TTL_X where ILC = 'hr';

create procedure getUsrObjicles(pUSR BIGINT, pILC CHAR(2))
begin
    select T_ART_L.*, TW.LABEL as WLABEL 
    from (
        select T_ART.*, TL.LABEL, TL.ILC
        from ( 
            select T1.ID, T1.TTL, T1.WHAT, T2.SRC 
            from USR_ENT as TE
            inner join OBJ as T1
            on T1.ID = TE.ENT
            inner join OBJ_IMG_DEF as T2
            on T1.OBJ = T2.OBJ
            where TE.USR = 3
            order by TE.TST desc
        ) as T_ART
        inner join TTL_X as TL
        on TL.ID = T_ART.TTL and TL.ILC = 'hr'
    ) as T_ART_L
    inner join TTL_X as TW
    on TW.ID = T_ART_L.WHAT and TW.ILC = T_ART_L.ILC
    ;
end :)


DELIMITER ;

call getUsrObjicles(3, 'hr');

select T1.*, 
    TIMG.SRC,
    coalesce(T2.LABEL, T3.LABEL, '??') as LABEL,
    coalesce(T4.LABEL, T5.LABEL, '??') as WLABEL
from OBJ as T1

inner join USR_ENT as UE
on UE.ENT = T1.ID and UE.USR = 3

inner join OBJ_IMG_DEF as TIMG
on TIMG.OBJ = T1.OBJ

left join TTL_ELEM as T2
on T2.TTL = T1.TTL and T2.ILC = 'hr'
left join TTL_1ST as T3
on T3.TTL = T1.TTL

left join TTL_ELEM as T4
on T4.TTL = T1.WHAT and T4.ILC = 'hr'
left join TTL_1ST as T5
on T3.TTL = T1.WHAT

order by UE.TST desc

limit 50;

where T1.WHAT is not null

--  full select 
select T1.*,
    coalesce(T2.LABEL, T3.LABEL, '??') as LABEL, 
    T3.STD, T3.STDABLE,
    coalesce(T4.LABEL, T5.LABEL, '??') as WLABEL
from (
    select T11.*, T13.SRC
    from
    (
        select ENT from USR_ENT where USR = 3
        order by TST
    ) as T12

    inner join OBJ as T11
    on T12.ENT = T11.ID

    inner join OBJ_IMG_DEF as T13
    on T13.OBJ = T11.OBJ
) as T1

left join TTL_ELEM as T2
on T2.TTL = T1.TTL and T2.ILC = 'hr'
left join TTL_1ST as T3
on T3.TTL = T1.TTL

left join TTL_ELEM as T4
on T4.TTL = T1.WHAT and T4.ILC = 'hr'
left join TTL_1ST as T5
on T3.TTL = T1.WHAT

limit 50

-- select id, image, label, wlabel for user articles listing
select T1.ID, T1.SRC,
    coalesce(T2.LABEL, T3.LABEL, notFound()) as LABEL, 
    coalesce(T4.LABEL, T5.LABEL, notFound()) as WLABEL
from (
    select T11.ID, T11.TTL, T11.WHAT, T13.SRC
    from
    (
        select ENT from USR_ENT where USR = 3
        order by TST
        limit 50
    ) as T12

    inner join OBJ as T11
    on T12.ENT = T11.ID

    inner join OBJ_IMG_DEF as T13
    on T13.OBJ = T11.OBJ
) as T1

left join TTL_ELEM as T2
on T2.TTL = T1.TTL and T2.ILC = 'hr'
left join TTL_1ST as T3
on T3.TTL = T1.TTL

left join TTL_ELEM as T4
on T4.TTL = T1.WHAT and T4.ILC = 'hr'
left join TTL_1ST as T5
on T3.TTL = T1.WHAT

-- select single article by id & language
select T1.*,
    coalesce(T2.LABEL, T3.LABEL, notFound()) as LABEL, 
    T3.STD, T3.STDABLE,
    coalesce(T4.LABEL, T5.LABEL, notFound()) as WLABEL
from (
    select T11.*, T12.SRC
    from
    (
        select * from OBJ where ID = 200001
        limit 1
    ) as T11

    inner join OBJ_IMG_DEF as T12
    on T12.OBJ = T11.OBJ
) as T1

left join TTL_ELEM as T2
on T2.TTL = T1.TTL and T2.ILC = 'hr'
left join TTL_1ST as T3
on T3.TTL = T1.TTL

left join TTL_ELEM as T4
on T4.TTL = T1.WHAT and T4.ILC = 'hr'
left join TTL_1ST as T5
on T3.TTL = T1.WHAT


-- select single article by id & language
select T1.*,
    coalesce(T2.LABEL, T3.LABEL, notFound()) as LABEL, 
    T3.STD, T3.STDABLE,
    coalesce(T4.LABEL, T5.LABEL, notFound()) as WLABEL
from (
    select T1.*, T2.SRC
    from
    (
        select * from OBJ where ID = 200001
        limit 1
    ) as T1

    inner join OBJ_IMG_DEF as T2
    on T2.OBJ = T1.OBJ
) as T1

left join TTL_ELEM as T2
on T2.TTL = T1.TTL and T2.ILC = 'hr'
left join TTL_1ST as T3
on T3.TTL = T1.TTL

left join TTL_ELEM as T4
on T4.TTL = T1.WHAT and T4.ILC = 'hr'
left join TTL_1ST as T5
on T3.TTL = T1.WHAT

-- list of titles
select T1.ID, coalesce(T2.LABEL, T3.LABEL, notFound()) as LABEL
from
(
    select T1.ID from TTL as T1
    inner join ENT as T2
    on T2.ID = T1.ID
    order by T2.TST desc
) as T1

left join TTL_ELEM as T2
on T2.TTL = T1.ID and T2.ILC = 'hr'
left join TTL_1ST as T3
on T3.TTL = T1.ID

limit 50

-- list of standard titles
select T1.ID, coalesce(T2.LABEL, T3.LABEL, notFound()) as LABEL
from
(
    select T1.ID from
    (
        select ID from TTL_INFO where STD = 1    
    ) as T1
    inner join ENT as T2
    on T2.ID = T1.ID
    order by T2.TST desc
) as T1

left join TTL_ELEM as T2
on T2.TTL = T1.ID and T2.ILC = 'hr'
left join TTL_1ST as T3
on T3.TTL = T1.ID

limit 50

-- title info of object
select T1.ID as OBJ, T2.*
from OBJ as T1
inner join TTL_INFO as T2
on T2.ID = T1.TTL

limit 50

--  listing of object whats

select T1.ID, coalesce(T2.LABEL, T3.LABEL, notFound()) as LABEL
from
(
    select ID from TTL where TPC = 'TQ'
) AS T1

left join TTL_ELEM as T2
on T2.TTL = T1.ID and T2.ILC = 'hr'
left join TTL_1ST as T3
on T3.TTL = T1.ID

limit 50

-- label of given title
select coalesce(T1.LABEL, T2.LABEL, notFound()) as LABEL
from (
    select TTL, LABEL from TTL_1ST
    where TTL = 105090
    limit 1
) as T1
left join TTL_ELEM as T2
on T2.TTL = T1.TTL and T2.ILC = 'hr'

