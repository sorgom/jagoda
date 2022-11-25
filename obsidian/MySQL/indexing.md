# MySQL indexing

## With table creation
```mysql
drop table if exists LOC_OBJ;
create table LOC_OBJ(
    OBJ BIGINT not null AUTO_INCREMENT,
    LOC BIGINT not null default 0,
    CNT INT,
    IDX int,
    NRS JSON,
    LABEL VARCHAR(128),
    primary key (OBJ, LOC),
    fulltext index(LABEL),
    index(CNT) using HASH
);
```

## Extern index
```mysql
create index LOC_OBJ_IDX on LOC_OBJ(IDX) using BTREE;
```

## Show / alter
**How to check available indexes?**

```mysql
SHOW INDEX FROM `tbl_student`
```

**How to remove indexes ?**

```mysql
DROP INDEX `student_index` ON `tbl_student`
```

**Specify index name**

```mysql
ALTER TABLE `tbl_student` ADD INDEX student_index (`student_id`)
```

Above statement will create an ordinary index with `student_index` name.

**Create unique index**

```mysql
ALTER TABLE `tbl_student` ADD UNIQUE student_unique_index (`student_id`)
```

Here, `student_unique_index` is the index name assigned to student_id and creates an index for which values must be unique (here null can be accepted).

**Full text option**

```mysql
ALTER TABLE `tbl_student` ADD FULLTEXT student_fulltext_index (`student_id`)
```

