from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'example'
app.config['MYSQL_DB'] = 'jagoda'
# Extra configs, optional:
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route("/")
def hello():
    cursor = mysql.connection.cursor()
    cursor.execute('select help_keyword_id from help_keyword')
    result = cursor.fetchall()
    cursor.close()
    data = [line[0] for line in result]
    return '<br>'.join(map(str, data))

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
