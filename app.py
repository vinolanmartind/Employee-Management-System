import pymysql
import mysql.connector
from flask import Flask,render_template,request,redirect,url_for



app=Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="martin",
    password="",
    database="employeemanagement_System"
)





@app.route('/login', methods=['GET','POST'] )
def login():
    if request.method == 'POST':

        empno = request.form['empno']
        password = request.form['Password']

        if empno == 'AJ68' and password == '2005':
            return redirect(url_for('employee_add'))
        else :
            return render_template ('login.html', error="Invalid Employee no or password ")
    return render_template("login.html")


@app.route('/employee_add', methods=['GET', 'POST'])
def employee_add():

    cursor = db.cursor(dictionary=True)
    cursor.execute("select Dep_Name from Department")
    departments = cursor.fetchall()
    cursor.close()
    success = None

    if request.method == 'POST':
        
        fname = request.form['FirstName']
        lname = request.form['LastName']
        dob = request.form['DOB']
        department = request.form['Department']
        designation = request.form['Designation']
        

        cursor = db.cursor()
        cursor.execute("INSERT INTO Employee ( Emp_FirstName, Emp_LastName, DateOFBirth, Department, Role ) VALUES (%s, %s, %s, %s, %s)",
                       (fname, lname, dob, department, designation ))
        db.commit()
        cursor.close()

        #return redirect(url_for('employee_view'))
        success = "Employee  successfully added!"

    return render_template("add_employee.html", departments=departments, active_page="employee_add", success=success)

@app.route('/employee_edit/<int:id>', methods=['GET', 'POST'])
def employee_edit(id):
     cursor = db.cursor(dictionary=True)
     cursor.execute("select Dep_Name from Department")
     departments = cursor.fetchall()
     cursor.close()
     success = None
     
   

     if request.method == 'POST':
            fname = request.form['Emp_FirstName']
            lname = request.form['Emp_LastName']
            dob = request.form['DateOFBirth']
            department = request.form['Department']
            designation = request.form['Role']

            cursor = db.cursor()
            cursor.execute("UPDATE Employee SET Emp_FirstName=%s, Emp_LastName=%s, DateOFBirth=%s, Department=%s, Role=%s WHERE Id=%s",
                           (fname, lname, dob, department, designation, id))
            db.commit()
            cursor.close()
            return redirect(url_for("employee_view"))
     
     cursor = db.cursor(dictionary=True)
     cursor.execute("SELECT * FROM Employee WHERE Id = %s", (id,))           
     employee = cursor.fetchone()
     cursor.close()
     success="Update Employee successfully!"
     success=success
    

    
     return render_template("edit_employee.html", active_page="employee_edit", departments=departments,employee=employee)

@app.route('/employee_view')
def employee_view():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()
    cursor.close()
    return render_template("view_employee.html", active_page="employee_view", employees=employees)






@app.route('/logout')
def logout():
    return render_template("login.html",active_page="logout")



if __name__ == '__main__':
    app.run(debug=True)