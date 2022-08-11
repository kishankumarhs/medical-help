
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
           ressp = make_response(redirect(url_for('home')))
           ressp.set_cookie('username',username)
           return ressp
       else:
            session['login_error'] ='Invalid Credentials'
            return redirect(url_for('login'))
    else:
        return render_template('index.html')

@app.route('/register',methods=['GET',"POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password =request.form['password']
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

    
if __name__ == '__main__':
   app.secret_key = 'asdsadaweasdasdar'
   app.run(debug=True)
   