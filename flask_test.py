import sqlite3

from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("welcome_page.html")

@app.route('/Add-Name/', methods=["GET", "POST"])
def add_name():
    if request.method == "POST":
        db_file = sqlite3.connect("User_db.db")
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        dob = request.form.get("DOB")
        db_file.execute(f"INSERT INTO Myself (FIRST_NAME,LAST_NAME,DOB) \
            VALUES ('{first_name}', '{last_name}', '{dob}')")
        db_file.commit()
        db_file.close()
        return redirect("/")
      
    return render_template("form.html") 

@app.route("/DOBList/")   
def dob_list():
    db_file = sqlite3.connect("User_db.db")
    list_users = db_file.execute("SELECT * FROM MYSELF")
    list_users = list(list_users)
    db_file.close()

    add_data_tag = '<br<br>><center style="font-size:20px"><a href="/Add-Name">Add Data</a></center>'
    home_tag = '<br><br><center style="font-size:20px"><a href="/">HOME</a></center>'
    return render_template("dob.html", dob_list = list_users) + home_tag + add_data_tag

@app.route("/delete/<sno>")
def delete_row(sno):
    DB_FILE = sqlite3.connect("User_db.db")
    DB_FILE.execute(f"DELETE FROM MYSELF WHERE SNO = {sno};")
    DB_FILE.commit()
    DB_FILE.close()
                
    return redirect("/DOBList/")

@app.route("/update/<sno>", methods=['GET', 'POST'])
def update_row(sno):
    if request.method == "POST":
        f_name = request.form["fname"]
        l_name = request.form["lname"]
        DOB = request.form["DOB"]
        DB_FILE = sqlite3.connect("User_db.db")
        DB_FILE.execute(f"UPDATE Myself set FIRST_NAME='{f_name}', LAST_NAME='{l_name}', DOB='{DOB}' where SNO = {sno}")
        DB_FILE.commit()
        DB_FILE.close()
        return redirect("/DOBList/")    
    return render_template("update.html", sno = sno) 

if __name__=='__main__':
    app.run(debug=True)