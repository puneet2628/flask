from flask import *
import pymysql
import pymysql.cursors

app  = Flask(__name__)
db_con = {
    "host":"localhost",
    "user":"root",
    "password":"admin",
    "database":"tbl_data",
}

@app.route('/')
def home():
    db  = pymysql.connect(**db_con)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from worksheet1")
    data = cursor.fetchall()
    return render_template('index.html',row=data)

@app.route('/delete/<int:id>',methods=['POST'])
def delete(id):
    con = pymysql.connect(**db_con)
    cursor = con.cursor(pymysql.cursors.DictCursor)
    cursor.execute("delete from worksheet1 where id=%s",(id))
    con.commit()
    cursor.close
    con.close()
    return redirect ('/')

if __name__ == "__main__":
    app.run(debug=True)