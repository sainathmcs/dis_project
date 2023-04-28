# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, jsonify, render_template, request, session
import sqlite3
import re
import asyncio

from smartrent import async_login

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.secret_key = ('FLASK_SECRET_KEY')

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.


@app.route("/dbhome")
def test_db():
    conn = sqlite3.connect('database.db')
    print('Opened database successfully', flush=True)
    conn.execute('DROP TABLE IF EXISTS Homes')
    conn.commit()
    conn.execute(
        'CREATE TABLE Homes (name TEXT, id TEXT ,address TEXT, rentid TEXT, password TEXT)')
    print('Table created successfully', flush=True)
    conn.close()
    return "Table created successfully"


@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    return render_template("index.html")


@app.route('/dashboard', methods=['POST', 'GET'])
# ‘/’ URL is bound with hello_world() function.
def dashboard():
    email = request.args.get('id')
    pwd = request.args.get('password')
    id = int(session['id'])
    return render_template("dashboard.html", email=email,pwd=pwd)


@app.route('/homedashboard')
# ‘/’ URL is bound with hello_world() function.
def homedashboard():
    return render_template("homedashboard.html")


@app.route('/Signup', methods=['POST', 'GET'])
# ‘/’ URL is bound with hello_world() function.
def Signup():
    if request.method == 'POST':
        email = request.form['usermail']
        password = request.form['pswd']
        # return "Saranyaa";
        if not password or not email:
            msg = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Please enter valid email'
        elif not len(password) > 6:
            msg = 'Your password should be more than 6 characters'
    # return "Saranyaaa"
    # return msg
        msg = ''
        if msg == '':
            with sqlite3.connect("database.db") as users:
                cursor = users.cursor()
                cursor.execute(
                    "INSERT INTO User(usermail,userpassword) VALUES(?,?) ", (email, password))
            users.commit()
        return render_template('login.html', msg="Account created successfully!!!")

    else:
        return render_template("signup.html")


@app.route('/about')
# ‘/’ URL is bound with hello_world() function.
def about():
    return render_template("about.html")


@app.route('/login', methods=["GET"])
# ‘/’ URL is bound with hello_world() function.
def login():
    msg = ''
    return render_template("login.html", msg=msg)


@app.route('/add-home')
# ‘/’ URL is bound with hello_world() function.
def addHomee():
    return render_template("addhome.html")


@app.route('/addHome', methods=["POST"])
# ‘/’ URL is bound with hello_world() function.
def addHome():
    name = request.form['name']
    address = request.form['address']
    rentid = request.form['rentid']
    password = request.form['password']
    ide = session['id']
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute(
            "INSERT INTO Homes(name,address,rentid,password,id) VALUES(?,?,?,?,?) ", (name, address, rentid, password, ide))
        cursor.execute("SELECT * FROM Homes WHERE id = ?", (ide,))
        homeList = cursor.fetchall()
    return render_template('homedashboard.html', homeList=homeList)


@app.route('/updateDeviceStatus', methods=["POST"])
# ‘/’ URL is bound with hello_world() function.
def updateDeviceStatus():
    data = request.get_json()
    uname = data['name']
    status = data['status']
    rentid = data['rentid']
    pwd= data['password']

    result = {'result': 'success'}
    if request.method == 'POST':
        print("status", status)
        asyncio.run(sm(uname, status, rentid, pwd))
    return jsonify(result)


@app.route("/login", methods=["POST"])
def login_post():
    # return "Saranya";
    msg = ''
    session.clear()
    if request.method == 'POST':
        email = request.form['usermail']
        password = request.form['pswd']
        # return "Saranyaa";
        if not password or not email:
            msg = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Please enter valid email'
        elif not len(password) > 6:
            msg = 'Your password should be more than 6 characters'
    # return "Saranyaaa"
    # return msg
        if msg == '':
            with sqlite3.connect("database.db") as users:
                cursor = users.cursor()
                cursor.execute(
                    "SELECT * FROM user WHERE usermail = ? AND userpassword = ?", (email, password))
                user = cursor.fetchone()

                if user:
                    session['id'] = user[0]
                    # session['user_id'] = user[0]
                    msg = 'Logged in successfully !'
                    ide = str(session['id'])
                    with sqlite3.connect("database.db") as users:
                        cursor.execute(
                        "SELECT * FROM Homes WHERE id = ?", (ide,))
                        homeList = cursor.fetchall()
                    return render_template('homedashboard.html', homeList=homeList)
                else:
                    msg = 'Incorrect username / password !'

        return render_template('login.html', msg=msg)

async def sm(device_name, device_status, uname, pwd):
    api = await async_login('sainath.mcs@gmail.com', 'sainathniz@SP20')
    if device_name == "lock":
        lock = api.get_locks()[0]
        locked = lock.get_locked()

        if locked == False:
            await lock.async_set_locked(True)
        if locked == True:
            await lock.async_set_locked(False)
        
        return True
    
    elif device_name == "thermostat":
        thermostat = api.get_thermostats()[0]
        mode = thermostat.get_mode()
        
        if mode == "off":
            await thermostat.async_set_mode("auto")
        elif "off":
            await thermostat.async_set_mode("off")
        
        return True
        
            
    
    



# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
