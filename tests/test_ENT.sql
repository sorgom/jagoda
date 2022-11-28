
SET foreign_key_checks = 0;

DROP TABLE IF EXISTS ENT;
CREATE TABLE ENT (
    ID BIGINT NOT NULL,
    TST TIMESTAMP not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    PRIMARY KEY (ID)
) ENGINE=INNODB;

DROP TABLE IF EXISTS WUMPEL;
CREATE TABLE WUMPEL (
    ID BIGINT NOT NULL,
    STD TINYINT NOT NULL DEFAULT 0,
    TPC CHAR(2) NOT NULL, 
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES ENT(ID) ON DELETE CASCADE
) ENGINE=INNODB;

drop function  if exists addWumpel;
DELIMITER :)  
create procedure addWumpel(pID bigint, pTPC CHAR(2))
BEGIN
    insert into ENT(ID) values (pID);
    insert into WUMPEL(ID, TPC) values (pID, pTPC);
END :)

DELIMITER ;
SET foreign_key_checks = 1;

-- GENERATED GRANT>
grant execute on procedure jagoda.addWumpel  to 'aut'@'%';

