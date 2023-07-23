from flask import Flask, request, render_template
import sqlite3
import re

 


app = Flask(__name__)


@app.route('/')
def main():
	return render_template("signup.html")

@app.route('/',methods=["GET","POST"] )
def user():
    
    return render_template("signup.html")

@app.route('/signin',methods=["GET","POST"] )
def signin():
    email = request.form.get("email")
    password = str(request.form.get("password"))
    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT email FROM user where email = (?) and password = (?) ",(email,password,)).fetchall()
    if len(result) >=1 :
        return render_template("secret.html")
 
    return render_template("signin.html")
    
@app.route("/signupform",methods=["GET","POST"])
def signup():
    f_name = request.form.get("firstname")
    l_name = request.form.get("lastname")
    email = request.form.get("email")  
    password = str(request.form.get("password"))
    confirmedpassword = request.form.get("confirmedpassword")
    exp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
          
    pattern = re.compile(exp)
    checking = re.search(pattern, password)
    
    if password == confirmedpassword:
        if checking:
            connection = sqlite3.connect("user.db")
            cursor = connection.cursor()
            result = cursor.execute("SELECT * FROM user where email = (?) ",(email,)).fetchall()
            if len(result) == 0:
                insert = "INSERT INTO user VALUES('{f_n}','{l_n}','{e_m}','{passw}','{con_pass}')".format(f_n = f_name,l_n= l_name,e_m = email,passw=password,con_pass=confirmedpassword)
                cursor.execute(insert)
                connection.commit()
                return render_template("thankyou.html")
            else:
                error = "User exists with same email Id"
                return render_template("signup.html",error=error)
        else :
            error = "Your Password does not meet the requirement"
            return render_template("signup.html",error=error)
           
    else:
        error = "password and confirmed password does not match"
        return render_template("signup.html",error=error)
    
    
 
        
        

if __name__=='__main__':
    app.run()

