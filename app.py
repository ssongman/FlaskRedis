from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql


app = Flask(__name__)
app.secret_key = "Secret Key"

def dbconnect():
    conn = pymysql.connect (host='172.30.1.31', port=30306, user='papa', password='papapass', db='papa', charset='utf8')
    return conn





@app.route('/')
def Index():   
    conn = dbconnect()
    cur = conn.cursor()

    sql='select * from data'
    cur.execute(sql)
    all_data = cur.fetchall()
    print(all_data)

    conn.close()

    return render_template("index.html", employees = all_data)


@app.route('/dbconntest')
def dbconntest():
    print("DB Connecting...")
    conn = dbconnect()

    flash("DB Connection Test is Successful")

    print("DB Closing...")
    conn.close()
    # return render_template("index.html")
    return redirect(url_for("Index"))



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = dbconnect()
        cur= conn.cursor()
        sql = f"insert into data (name, email, phone) values ('{name}','{email}','{phone}')"
        cur.execute(sql)
        conn.commit()
        conn.close()

        flash("Employee inserted Successfully")

    return redirect(url_for("Index"))


@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        
        conn = dbconnect()
        cur= conn.cursor()
        sql = f"update data set name='{name}', email='{email}', phone='{phone}' where id = {id}"
        cur.execute(sql)
        conn.commit()
        conn.close()

        flash("Employee updated Successfully")

    return redirect(url_for("Index"))


@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete(id):
    if request.method == 'GET':
        
        conn = dbconnect()
        cur= conn.cursor()
        sql = f"delete from data where id = {id}"
        cur.execute(sql)
        conn.commit()
        conn.close()

        flash("Employee deleted Successfully")

    return redirect(url_for("Index"))




if __name__ == "__main__":
    app.run(port=5001, debug=True)
