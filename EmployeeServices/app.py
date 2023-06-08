from flask import Flask,flash,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

app.secret_key = 'xyzsdfg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'employes_service'



mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM login WHERE email = %s AND password = %s", (email, password))
        data = cursor.fetchone()
        if data:
            session['loggedin'] = True
            session['email'] = data['email']
            session['password']=data['password']
            message = 'Logged in Successfully !'
            return redirect(url_for('dashboard',message=message))
        else:
            message = 'Please enter correct email / password !'
            # return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        return render_template('dashboard.html',employees=employees)
    else:
        return redirect(url_for('login'))



@app.route('/register', methods=['GET','POST'])#This is the page for adding student information to DB
def register():
    msg=''
    if request.method == 'POST'and 'empid' in request.form and 'name' in request.form and 'email' in request.form and 'position' in request.form and 'phone' in request.form and 'location' in request.form:
        Empid=request.form['empid']
        Name = request.form['name']
        Email = request.form['email']
        Position = request.form['position']
        Phone = request.form['phone']
        Location = request.form['location']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employees WHERE email = %s ',(Email,))
        result = cursor.fetchone()
        
        if result:
            msg = 'employee already exists !'
           
        else:
            cursor.execute("INSERT INTO employees VALUES(%s,%s,%s,%s,%s,%s)",(Empid,Name,Email,Position,Phone,Location))
            mysql.connection.commit()

            msg='Employees registered !'
            

    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('register.html',msg=msg)
    

@app.route('/view', methods=['GET','POST'])
def view():
    if 'loggedin' in session:
        viewid=request.args.get('empid')
        print(viewid)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM employees WHERE empid= {}".format(viewid))
        employees = cursor.fetchone()
        return render_template('view.html',employees=employees)
    return redirect(url_for('login'))



@app.route('/update', methods=['GET','POST'])
def update():
    msg=''
    if request.method == 'POST' and 'empid' in request.form and 'name' in request.form and 'position' in request.form and 'phone' in request.form and 'location' in request.form:
        Empid=request.form.get('empid')
        Name = request.form['name']
        Position = request.form['position']
        Phone = request.form['phone']
        Location = request.form['location']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employees WHERE empid = %s',(Empid,))
        result = cursor.fetchone()
        
        if result:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE employees SET name=%s, position=%s,phone=%s,location=%s WHERE empid= %s",(Name,Position,Phone,Location,Empid)) 
            print(Name,Position,Phone,Location)
            msg='Employees details Updated Successfully !'
            mysql.connection.commit()
                
        else:
            msg = 'Employee details not updated !'
    
        
    return render_template('update.html',msg=msg)
    


@app.route('/delete', methods=['GET','POST'])
def delete():
    if 'loggedin' in session:
        deleteid=request.args.get('empid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM employees WHERE empid= {}".format(deleteid))
        mysql.connection.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
    

if __name__ == "__main__":
    app.run(debug=True)

