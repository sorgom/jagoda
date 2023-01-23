print('start')
import pymysql.cursors

print('connect')
connection = pymysql.connect(host='127.0.0.1',
                             user='aut',
                             password='** yes: i am an author **',
                             database='jagoda',
                            # charset='utf8mb4',
                            #  cursorclass=pymysql.cursors.DictCursor
                             )


print('select')
with connection.cursor() as cursor:
        # Read a single record
        sql = 'call getObjsNoWhat(%s)'
        cursor.execute(sql, ('fr',))
        result = cursor.fetchall()
        print(len(result))

print('close')
connection.close()

print('connect')
connection = pymysql.connect(host='127.0.0.1',
                             user='aut',
                             password='** yes: i am an author **',
                             database='jagoda',
                             charset='utf8mb4',
                            #  cursorclass=pymysql.cursors.DictCursor
                             )

print('select')
with connection.cursor() as cursor:
        # Read a single record
        sql = 'select ILC, LABEL from LANG order by ORD'
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)

print('close')
connection.close()