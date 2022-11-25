drop table if exists LOC_OBJ;
create table LOC_OBJ(
    OBJ BIGINT not null AUTO_INCREMENT,
    LOC BIGINT not null default 0,
    CNT INT,
    NRS JSON,
    LABEL VARCHAR(128),
    primary key (OBJ, LOC),
    fulltext index(LABEL),
    index(CNT)
);

insert into LOC_OBJ(OBJ, NRS) values (123, '[ 1, 12, 14, 99]');

update LOC_OBJ set NRS = '[ 1, 12, 99, 101 ]' where OBJ = 123;
