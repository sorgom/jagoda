drop table if exists TEST;
create table TEST(
    OBJ BIGINT not null AUTO_INCREMENT,
    LOC BIGINT not null default 0,
    CNT INT,
    IDX int,
    NRS JSON,
    LABEL VARCHAR(128),
    CONT LONGTEXT,
    primary key (OBJ, LOC),
    fulltext index(LABEL),
    index(CNT) using HASH
);

create index TEST_IDX on TEST(IDX) using BTREE;

insert into TEST(OBJ, NRS) values 
    (123, '[ 1, 12, 14, 99]'),
    (124, '100')
    ;

update TEST set NRS = '[ 1, 12, 99, 101 ]' where OBJ = 123;
