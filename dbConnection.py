import mysql.connector as ab
mydb=ab.connect(user='akshat', password='root',host='localhost',database="restraunt")
mycursor = mydb.cursor()
'''if con.is_connected():
    print("Connection successful..!")
    print(con)'''

'''mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)'''
def password(pas):
    mycursor.execute("SELECT * FROM owner_pass")
    result = mycursor.fetchall()
    for row in result:
        if(pas==row[0]):
            return 1
        else:
            return 0
def password_change():
    new_pass = input("Enter new password: ")
    confirm_pass = input("Re-enter the same password: ")
    if new_pass == confirm_pass:
        mycursor.execute("DROP TABLE IF EXISTS owner_pass;")
        mycursor.execute("CREATE TABLE owner_pass (pass VARCHAR(20) NOT NULL UNIQUE);")
        sql = "INSERT INTO owner_pass (pass) VALUES (%s);"
        mycursor.execute(sql, (new_pass,))
        mydb.commit()
        print("Password changed successfully.")
    else:
        print("Passwords do not match. Please try again.")
        password_change()


    
def insert_empl_info(Name, emp_id, password, contact_no, address):
    if check_id(emp_id):
        remove_emp(emp_id)
    sql = "INSERT INTO employee_information (Name, id, pass, contact_no, address) VALUES (%s, %s, %s, %s, %s)"
    val = (Name, emp_id, password, contact_no, address)
    mycursor.execute(sql, val)
    mydb.commit()


def view_emp_info():
    mycursor.execute("SELECT * FROM employee_information")
    result = mycursor.fetchall()
    print('Name\t  id\t password\t contact_no\t address')
    for row in result: 
        for i in row:
            print(i,end='\t')
        print('\n')

def check_id(id):
    mycursor.execute("SELECT * FROM employee_information")
    result = mycursor.fetchall()
    for row in result:
        if(id==row[1]):
            return 1
    return 0
def check_pass(password):
    mycursor.execute("SELECT * FROM employee_information")
    result = mycursor.fetchall()
    for row in result:
        if(password==row[2]):
            return 1
    return 0

def remove_emp(id):
    sql="delete from employee_information where id=(%s)"
    val=(id,)
    mycursor.execute(sql,val)
    mydb.commit()

    
def input_menu(dish,price):
    sql = "INSERT INTO menu (dish, price) VALUES (%s, %s)"
    val = (dish,price)
    mycursor.execute(sql, val)
    mydb.commit()


def view_menu():
    mycursor.execute("SELECT * FROM menu")
    result = mycursor.fetchall()
    print("DISH \tPRICE(INR)")
    for row in result:
        for i in row:
            print(i,end='\t')
        print('\n')
def remove_menu(dish1):
    sql="delete from menu where dish=(%s)"
    val=(dish1,)
    mycursor.execute(sql,val)
    mydb.commit()
def menu_price(dish,price):
    sql="update menu set price = %s  where dish =%s"
    val=(price,dish)
    mycursor.execute(sql,val)
    mydb.commit()

def check_menu(dish):
    mycursor.execute("SELECT * FROM menu")
    result = mycursor.fetchall()
    for row in result:
        if(dish==row[0]):
            return 1
    return 0

def remove_menu(dish):
    sql="delete from menu where dish=(%s)"
    val=(dish,)
    mycursor.execute(sql,val)
    mydb.commit()

def input_recipt(Name,buyer,contact1_no,total):
    sql = "INSERT INTO recipt (Name,buyer,contact1_no,total) VALUES (%s, %s,%s,%s)"
    val = (Name,buyer,contact1_no,total)
    mycursor.execute(sql, val)
    mydb.commit()

def view_recipt():
    mycursor.execute("SELECT * FROM recipt")
    result = mycursor.fetchall()
    for row in result: 
        print(row,'\n') 

def emp_pass(emp_id,new_pass):
    try:
        sql = "UPDATE employee_information SET pass = %s WHERE id = %s"
        mycursor.execute(sql, (new_pass, emp_id))
        mydb.commit()
        print("Password changed successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def cal_bill(item,quan):
    mycursor.execute("SELECT * FROM menu")
    result = mycursor.fetchall()
    for row in result:
        if item==row[0]:
            return quan*row[1]


  


