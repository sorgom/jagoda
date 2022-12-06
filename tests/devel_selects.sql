
-- T1 ART OBJ
-- T2 OBJ ID TTL ...
-- T3 TTL_ELEM_X -> TTL_X ID ILC LABEL
-- T4 TTL_INFO -> ID TPC STDABLE STD
-- T5 TTL_ELEM_X -> TTL_X ID ILC LABEL
-- T6 OBJ_IMG_DEF OBJ SRC

drop view if exists ART_X;
create view ART_X as
select T1.*, T2.*, T3.ILC, T3.LABEL, T4.STD, T4.STDABLE, T5.LABEL as WLABEL, T6.SRC
from ART as T1
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

drop procedure if exists getUsrArticles;
DELIMITER :)  

CREATE TEMPORARY VIEW LX as
select ID, LABEL
from TTL_X where ILC = 'hr';

create procedure getUsrArticles(pUSR BIGINT, pILC CHAR(2))
begin
    select T_ART_L.*, TW.LABEL as WLABEL 
    from (
        select T_ART.*, TL.LABEL, TL.ILC
        from ( 
            select T1.ID, T1.TTL, T1.WHAT, T2.SRC 
            from USR_ENT as TE
            inner join ART_OBJ as T1
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

call getUsrArticles(3, 'hr');

select T1.*, 
    TIMG.SRC,
    coalesce(T2.LABEL, T3.LABEL, '??') as LABEL,
    coalesce(T4.LABEL, T5.LABEL, '??') as WLABEL
from ART_OBJ as T1

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

select T1.*,
    coalesce(T2.LABEL, T3.LABEL, '??') as LABEL, 
    T3.STD,
    coalesce(T4.LABEL, T5.LABEL, '??') as WLABEL
from (
    select T11.*, T13.SRC
    from
    (
        select ENT from USR_ENT where USR = 3
        order by TST
    ) as T12

    inner join ART_OBJ as T11
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
