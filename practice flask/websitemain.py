from flask import *
import pymysql
import pymysql.cursors

app = Flask(__name__)

db_con = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "websitedata",
}

# home page
@app.route('/')
def home():
    return render_template("website.html")

#page after the login page for admin btn
@app.route('/1')
def site1():
    return render_template("website1.html")


# login page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form['nme']
        email = request.form['eml']
        password = request.form['pwd']
        mobile = request.form['mn']

        # Open the database connection
        con = pymysql.connect(**db_con)
        cur = con.cursor(pymysql.cursors.DictCursor)
        
        # Correcting the SQL query by removing the extra comma
        cur.execute("INSERT INTO login_data (name, email, password, mobile) VALUES (%s, %s, %s, %s)", (name, email, password, mobile))
        
        # Commit the changes and close the connection
        con.commit()
        cur.close()
        con.close()
        
        return redirect('/1')
    
    return render_template("websitelogin.html")

#admin login form page

@app.route('/adminlogin',methods=["GET","POST"])
def adminlogin():
    if request.method == "POST":
        username = request.form['aun']
        password = request.form['pwd']

        if username=="root" and password =="root":
            return redirect('/adminpannel')
        else:
            return "User Name Or Password Not Valid"
    else:
        return render_template('websiteadminform.html')


# admin Pannel after admin login
@app.route('/adminpannel')
def adminpannel():
    con = pymysql.connect(**db_con)
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute("select * from login_data")
    data =cur.fetchall()
    return render_template('websiteadminpannel.html',row=data)

# delete the user from the database from ui
@app.route('/deleteuser/<int:id>', methods=["GET", "POST"])
def deleteuser(id):
    con = pymysql.connect(**db_con)
    cur = con.cursor(pymysql.cursors.DictCursor)
    
    # Correct the SQL query to delete the user based on the ID
    cur.execute("DELETE FROM login_data WHERE id = %s", (id,))
    
    con.commit()
    cur.close()
    con.close()
    
    return redirect('/adminpannel')  # Redirect to admin panel after deletion


# update the user from the database from ui
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
        con = pymysql.connect(**db_con)
        cur = con.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            name= request.form.get('name')
            email = request.form.get('email')
            password=request.form.get('password')
            mobile = request.form.get('mobile')

            if not all([name, email, password, mobile]):
                return "All fields are mandatory"

            cur.execute('UPDATE login_data SET name=%s, email=%s, password=%s, mobile=%s WHERE id=%s', (name, email, password, mobile, id))

            con.commit()
            cur.close()
            con.close()
            return redirect('/adminpannel')
        else:
            cur.execute("select * from login_data where id=%s",(id))
            user_data= cur.fetchone()
            cur.close()
            con.close()
            return render_template("websiteuserupdate.html" , row=user_data)

    
if __name__ == "__main__":
    app.run(debug=True)
