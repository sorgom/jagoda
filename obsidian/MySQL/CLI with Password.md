```shell
mysql -h 127.0.0.1 -P 3306 -u root --password=rr jagoda < init_functions.sql
mysql -h 127.0.0.1 -P 3306 -u root -prr jagoda < init_functions.sql
cat *.sql | mysql -h 127.0.0.1 -P 3306 -u root -prr jagoda
```


