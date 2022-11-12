select OBJECT, IMG, ORD from OBJECT_IMG as OI
inner join
(select OBJECT as O, min(ORD) as MO from OBJECT_IMG GROUP BY OBJECT) as OO
ON OI.OBJECT = O AND OI.ORD = MO