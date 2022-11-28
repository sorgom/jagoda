## Goal
Make sure that certain columns cannot be modified after creation.
## Approach
Grant or revoke update privilage for columns concerned

https://dev.mysql.com/doc/refman/8.0/en/grant.html#grant-column-privileges

```
GRANT SELECT (col1), INSERT (col1, col2) ON mydb.mytbl TO 'someuser'@'somehost';
```

### Summary
### Privileges
It is possible to grant column wise.
E.g.
```
GRANT UPDATE (STD) ON jagoda.TTL TO 'wumpel'@'%';
```

It is NOT POSSIBLE to grant privileges table wise and then revoke column wise.
E.g. this will not work:
```
GRANT UPDATE ON jagoda.TTL TO 'wumpel'@'%';
REVOKE UPDATE (TPC) ON jagoda.TTL FROM 'wumpel'@'%';
```

### Update / Replace Into
It is possible to use "replace into" a table even when not apdatable columns concerned.
