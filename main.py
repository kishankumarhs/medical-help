
from json import JSONEncoder
from flask import Flask,render_template,request,redirect,url_for,make_response,session,flash
from DB import connectDB
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if request.cookies.get('username'):
        return render_template('dashbord.html')
    else:
       return redirect(url_for('login')) 

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
       username =  request.form['username']
       password = request.form['password']
       conn = connectDB()
       mycursor = conn.cursor()
       sql = 'SELECT * FROM users WHERE username = %s AND password = %s'
       val = (username,password)
       mycursor.execute(sql,val)
       myresult = mycursor.fetchall()
       if len(myresult) > 0 and myresult[0][1] == username and myresult[0][2] == password:
           if myresult[0][3] == 1 :
                user = {
                    "id":myresult[0][0],
                    "username":myresult[0][1],
                    "isadmin":myresult[0][3]
                }
                ressp = make_response(redirect(url_for('admin')))
                ressp.set_cookie('username',username)
                return ressp
           ressp = make_response(redirect(url_for('home')))
           ressp.set_cookie('username',username)
           return ressp
       else:
            error ='Invalid Credentials'
            return render_template('index.html',error=error)
    else:
        return render_template('index.html',error=error)

@app.route('/register',methods=['GET',"POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password =request.form['password']
        if username == '' or password == '':
            flash('Please fill all the fields')
            return redirect(url_for('register'))
        conn = connectDB()
        sql  ='INSERT INTO users (username,password) VALUES (%s,%s)'
        val = (username,password)
        mycursor = conn.cursor()
        mycursor.execute(sql,val)
        # return mycursor.rowcount
        conn.commit()
        ressp = make_response(redirect(url_for('home')))
        ressp.set_cookie('username',username)
        return ressp
    else:
        return render_template('register.html')

@app.route("/logout",methods = ["POST"])
def logout():
    ressp = make_response(redirect(url_for('login')))
    ressp.set_cookie('username','')
    return ressp

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route("/api/getuser/<userid>")
def getuser(userid):
    if userid != '':
        # return userid
        conn = connectDB()
        mycursor = conn.cursor()
        sql = 'SELECT * FROM users WHERE username = `%s`'
        val = userid
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        conn.commit()
        if len(myresult)>0:
            return myresult
        # user = {
        #     'id':myresult[0][0],
        #     'username':myresult[0][1],
        #     'password':myresult[0][2],
        #     'isadmin':myresult[0][3]
        # }
        return 'Not Found'

if __name__ == '__main__':
   app.secret_key = 'asdsadaweasdasdar'
   app.run(debug=True)
   
