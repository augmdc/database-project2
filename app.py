from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="T1nT1nMDC",
 database="clinic_db"
)

print(mydb)

@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
     query = request.form['query']
     cursor = mydb.cursor()
     cursor.execute(query)
     result = cursor.fetchall()
     return render_template('index.html', result=result)
  else:
     return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)

