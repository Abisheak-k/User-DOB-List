from flask import Flask, request, render_template, redirect
from datetime import datetime, date
import csv
DOB_file = "DOB.csv"

app = Flask(__name__)
        
@app.route('/')
def welcome():
   return render_template("welcome_page.html")

@app.route('/Add-Name/', methods = ["GET", "POST"])
def add_name():
   if request.method == "POST":
      first_name = request.form.get("fname")
      last_name = request.form.get("lname")
      DOB = request.form.get("DOB")
      print(DOB, type(DOB))
      with open(DOB_file, 'a') as dob:
         writer = csv.writer(dob)
         writer.writerow([first_name, last_name, DOB])
      return redirect("/")
      
   return render_template("form.html") 

@app.route("/DOBList/")   
def dob_list():
   dic = {}
   with open(DOB_file, 'r') as db:
      reader = csv.DictReader(db)
      for i in reader:
         dic[i['FirstName']] = list(i.values())
         
   add_data_tag = '<br<br>><center style="font-size:20px"><a href="/Add-Name">Add Data</a></center>'
   home_tag = '<br><br><center style="font-size:20px"><a href="/">HOME</a></center>'
   return render_template("dob.html", dob_list = dic) + home_tag + add_data_tag

@app.route("/delete/<name>")
def delete_row(name):
   with open(DOB_file, 'r') as file:
      dob_list = csv.reader(file)
      dob_list = list(dob_list)
      for dob in dob_list:
         if name == dob[0]:
            dob_list.remove(dob)
      print(dob_list)
            
   with open(DOB_file, 'w+') as file:
      writer = csv.writer(file)
      writer.writerows(dob_list)            
            
   return redirect("/DOBList/")

@app.route("/update/<name>", methods=['GET', 'POST'])
def update_row(name):
   if request.method == "POST":
      print("hello")
      first_name = request.form.get("fname")
      last_name = request.form.get("lname")
      DOB = request.form.get("DOB")
      with open(DOB_file, 'r') as file:
         dob_list = csv.reader(file)
         dob_list = list(dob_list)
         for i, dob in enumerate(dob_list):
            if name == dob[0]:
               dob_list[i] = [first_name, last_name, DOB]
               
      with open(DOB_file, 'w+') as  file:
         writer = csv.writer(file)
         writer.writerows(dob_list)
      return redirect("/DOBList/")    
   return render_template("update.html", name=name) 

if __name__=='__main__':
   app.run(debug=True)