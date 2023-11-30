from flask import Flask, request, render_template, session, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your secret key'

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
      host = request.form['host']
      user = request.form['user']
      password = request.form['password']
      database = request.form['database']
      session['host'] = host
      session['user'] = user
      session['password'] = password
      session['database'] = database
      return redirect(url_for('home'))
  else:
      return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def home():
  if not session.get('host') or not session.get('user') or not session.get('password') or not session.get('database'):
      return redirect(url_for('login'))
  else:
      mydb = mysql.connector.connect(
          host=session['host'],
          user=session['user'],
          password=session['password'],
          database=session['database']
      )
      if request.method == 'POST':
          query = request.form['query']
          cursor = mydb.cursor()
          cursor.execute(query)
          result = cursor.fetchall()
          column_names = [desc[0] for desc in cursor.description]
          return render_template('index.html', result=result, column_names=column_names)
      else:
          return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)


