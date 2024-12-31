from flask import *
import pymysql
import pymysql.cursors

app = Flask(__name__)

db_con = {
    "host":"localhost",
    "user":"root",
    "password":"admin",
    "database":"tbl_data"
}


@app.route("/")
def home():
    con = pymysql.connect(**db_con)
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute("select * from worksheet1")
    dta = cur.fetchall()
    return render_template("useradmintable.html",data=dta)

@app.route('/delete/<int:id>',methods=["POST"])
def delete(id):
    con = pymysql.connect(**db_con)
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute("delete from worksheet1 where id=%s",(id))
    con.commit()
    cur.close()
    con.close()
    return redirect('/')

@app.route("/add",methods = ["GET","POST"])
def add():
    con = pymysql.connect(**db_con)
    cur = con.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        name = request.form.get("name")
        age = request.form.get("age")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        password = request.form.get("password")


        if not all([name,age,mobile,email,password]):
            return "all fields are mendatory" ,789
        cur.execute(""" 
                    insert into worksheet1 (name,age,mobile,email,password)
                    values(%s,%s,%s,%s,%s)
                    """,(name,age,mobile,email,password))
        con.commit()
        cur.close()
        con.close()
        return redirect('/')
    else:
        cur.close()
        con.close()
        return render_template("add.html")
if __name__ == "__main__":
    app.run(debug=True)