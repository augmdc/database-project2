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
            if 'Appointments' in request.form:
                query = "SELECT CONCAT(p.First_name, ' ', p.Last_name) as Patient_name, a.Assessment_Name, CONCAT(p2.First_name, ' ', p2.Last_name) as Staff_name, ap.Total_cost FROM appointment as ap, assessment as a, person as p, person as p2 WHERE ap.AssessmentID = a.AssessmentID and p.PersonID = ap.PatientID and p2.PersonID = ap.StaffID and ap.status = 'Not Complete'"
            elif 'Medication Stock' in request.form:
                query = "select Medication_name, Stock, Unit, Cost_per_unit from medication order by Stock"
            elif 'Staff Qualifications' in request.form:
                query = "select q.Qualification_Name, CONCAT(p.First_name, ' ', p.Last_name) as Staff_name, q.Expiry_date from qualification as q, person as p where q.StaffID = p.PersonID"
            else:
                query = request.form['query']

            cursor = mydb.cursor()
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                return render_template('index.html', result=result, column_names=column_names)
            except:
                print("No query inserted!")
                return render_template('index.html')
        else:
            return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)


