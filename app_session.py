from flask import Flask, session, redirect, url_for, escape, request, render_template

app = Flask(__name__, template_folder='templates')

langs = (
    (100, 'English'),
    (101, 'Deutsch'),
    (102, 'Francais')
)

@app.route('/')
def index():
    output = []
    output.append('Logged in as %s' % escape(session['username']) if 'username' in session else 'not logged in')
    output.append('language: %s' % escape(session['language']) if 'language' in session else 'no language')
    return '<br>'.join(output)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
             <p><input type=text name=username /></p>
            <p><input type=submit value=Login /></p>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lang', methods=['GET', 'POST'])
def lang():
    if request.method == 'POST':
        session['language'] = request.form['language']
        return redirect(url_for('index'))
    return render_template('language.htm', langs=langs)

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=False)