import mysql.connector

config = {
  'user': 'aut',
  'password': 'aa',
#   'host': '127.0.0.1',
  'database': 'jagoda',
  'autocommit': True
}

cnx = mysql.connector.connect(**config)

try:
    cursor = cnx.cursor()
    cursor.callproc('addTtl', [103, 'OT'])
    cursor.close()
except:
    pass

cursor = cnx.cursor(dictionary=True)
cursor.execute('select * from ENT;')
data = cursor.fetchall()
cursor.close()


print('... >>')
cursor = cnx.cursor()
cursor.execute('select nextId()', ())
next = cursor.fetchone()[0]
print('next', next)
# cursor = cnx.cursor()
stmt0 = 'insert into ENT(ID) values (%s)'
data0 = (next,)
stmt1 = 'insert into TTL(ID, TPC) values (%s, %s)'
data1 = (next, 'OT')
print(0)
cursor.execute(stmt0, data0)
print(1)
cursor.execute(stmt1, data1)
cursor.close()
# cnx.commit()
print('<< ...')

sql = 'select * from ENT'
params = ()
cursor = cnx.cursor(dictionary=True)
cursor.execute(sql, params)
data = cursor.fetchall()
cursor.close()

print('len:', len(data))


# cursor = cnx.cursor()
# stmt = 'select nextId()'
# cursor.execute(stmt, ())
# res = cursor.fetchone()[0]
# cursor.close()
# print('next:', res)

# # print(data)

# # cursor = cnx.cursor()
# # res = cursor.callproc('test')
# # # data = cursor.fetchall()
# # cursor.close()

# print(res)

# cnx.close()


# class MyDB(object):
#     def __init__(self, getUidFunc, config):
#         self.getUid = getUidFunc
#         self.cnx = mysql.connector.connect(**config)

#     def __del__(self):
#         self.cnx.close()

# # db = MyDB('wumpel', config)