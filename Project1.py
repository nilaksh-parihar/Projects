import random
import time
from datetime import datetime as dt
import dbConnection as file2
import mysql.connector as ab
mydb=ab.connect(user='akshat', password='root',host='localhost',database="restraunt")
mycursor = mydb.cursor()


orders = {}
def info():
    user=input('OWNER or EMPLOYEE : ').lower()
    if (user == 'owner') :
        pass_wrd=input("Enter password :")
        print()
        if file2.password(pass_wrd):
            print("Welcome Sir \n")
            owner()
        else:
            print("Invalid passsword\n")
            info()
    elif(user == 'employee'):
        employee()
    else:
        print('Invalid choice')
        info()


def owner():
    print('''\npress 1-->Fetch employee information
press 2-->Edit employee information
press 3-->Change password
press 4-->Display Menu
press 5-->Change menu
press 6--> view sales 
press 7-->Back to user login\n''')
    owner_choice=int(input("Enter your choice :"))
    if (owner_choice==1):
        emp_info()
    elif (owner_choice==2):
        emp_edit()
    elif (owner_choice==3):
        pass_wrd=input("Enter original password :")
        if  file2.password(pass_wrd) :
            file2.password_change()
            owner()
        else:
            print("invalid password ")
    elif(owner_choice==4):
        menu_print()
    elif(owner_choice==5):
        menu_change()
    elif(owner_choice==7):
        info()
    elif (owner_choice==6):
        file2.view_recipt()
    else:
        print("invalid choice")
        owner()

def employee_choice():
    print('''\nPress 1->Add order
press 2->Change Password
press 3->Go back
press 4->Exit''')
    emp_choice=input("Enter Your Choice : ")
    if emp_choice=='1':
        add_order()
    elif emp_choice=='2':
        empl_username=input("Enter your user id :")
        old_pas=input("Enter your old password : ")
        
        if(employee_login(empl_username,old_pas)):
            changeemp_pass(empl_username)
    elif emp_choice=='3':
        end = time.time()
        #print(int(end - start))
        employee()
    elif emp_choice=='4':
        exit
    else:
        print("invalid choice ! try again")
        employee_choice()
    

def changeemp_pass(empl_username):
    new_pass=input("Enter new password :")
    confirm_pass=input("Re-enter the same password : ")
    
    if new_pass==confirm_pass:
        file2.emp_pass(empl_username,new_pass)
        employee_choice()
    else:
        print("Password don't match")
        changeemp_pass()


        
def emp_info():
    file2.view_emp_info()
    owner()

def emp_edit():
    print("""\npress 1--> add employee
press2-->remove employee
press3-->edit employee info
press4-->exit\n""")
    o_choice=int(input("enter your choice :"))
    if(o_choice==1):
        new_emp=input("name of the new employee :")
        new_con=input("enter contact number :")
        new_add=input("enter address :")
        new_pass=new_emp[:2]+"123"
        new_id = new_emp + ''.join(str(random.randint(0, 9)) for _ in range(3))
        file2.insert_empl_info(new_emp,new_id,new_pass,new_con,new_add)
        print(f"{new_emp} got the job ")
        emp_edit()
    elif(o_choice==2):
        emp_id=input("enter employee id :")
        if file2.check_id(emp_id):
            file2.remove_emp(emp_id)
        else:
            print(f"{emp_id} does not exist")
        emp_edit()
    elif(o_choice==3):
        emp_id=input("enter the employe id")
        if(file2.check_id(emp_id)):
            new_emp=input("name of the employee :")
            new_con=input("enter contact number :")
            new_add=input("enter address :")
            new_pass=new_emp[:2]+"123"
            file2.insert_empl_info(new_emp,emp_id,new_pass,new_con,new_add)
        else:
            print(f"{emp_id} does not exist")
        emp_edit()
    elif(o_choice==4):
        owner()
    else:
        print("invalid choice")
        emp_edit()


def menu_print():
    file2.view_menu()
    owner()


def menu_change():
    global menu
    print('''\npress 1-->Add dishes
press 2-->Remove dishes
press 3-->Change prices
press 4 -->Exit\n''')
    menu_choice=int(input("enter your choice-->"))
    if menu_choice==1:
        new_dish=input("enter the name of the dish :" )
        new_price=int(input("enter the price :"))
        file2.input_menu(new_dish,new_price)
        print(f"{new_dish} added succesfully !!")
        menu_change()
    elif menu_choice==2:
        dish_name=input("enter the name of the dish :")
        if file2.check_menu(dish_name):
            file2.remove_menu(dish_name)
        else:
            print(f"{dish_name} does not exist")
        menu_change()
    elif menu_choice==3:
        old_dish=input("enter the dish name : ")
        if(file2.check_menu(old_dish)):
            new_price=int(input("enter the prices :"))
            file2.menu_price(old_dish,new_price)
        else:
            print(f"{old_dish} does not exist")
        menu_change()
    elif menu_choice==4:
        owner()
    else:
        print("invalid choice")
        menu_change()


def employee_login(id, password):
    if file2.check_id(id):
        if file2.check_pass(password):
            return True
        else:
            return False
    else:
        return False


def calculate_bill():
    total = 0
    for i in orders.keys():
        bil=file2.cal_bill(i,orders[i])
        total+=bil
    print(f"Total bill: {total}")
    return total


def display_order():
    print("Current Order:")
    for item, quantity in orders.items():
        print(f"{item}: {quantity}")


def change_order():
    global orders
    a=0
    option="yes"
    while(a!=4) :
        a=int(input("What would You like to do \n1.Remove \n2.Change Quantity \n3.Add \n4.Exit : "))
        print()
        if a==1:
            rem=input("You want to remove : ")
            if rem not in orders.keys():
                print("invalid item")
                continue
            orders.pop(rem)
            display_order()
        elif a==2:
            item=input("Which Item's quantity you want to change :")
            qty=int(input("Quantity you want to change : "))
            orders[item]=qty
            display_order()
        elif a==3:
            while option == 'yes':
                item=input("Item : ")
                if not(file2.check_menu(item)):
                    print("The item is not in the menu ! ")
                    continue
                quantity=int(input("Quantity : "))
                orders[item]=quantity
                option=input("Add more (yes,no) : ")
                display_order()
        else:
            print("invalid choice")


employee_id=""
def employee():
    # Employee Login
    while True:
        global employee_id
        employee_id = input("Enter employee id: ")
        employee_password = input("Enter employee password: ")
        if employee_login(employee_id, employee_password):
            print("Employee login successful.")
            global start
            start = time.time()
            employee_choice()
        else:
            print("Invalid employee credentials.")

    # Customer Details
def add_order():    
    print("\nCustomer Details:")
    customer_name = input("Customer name : ")
    customer_no=input("Contact number : ")
   
    print()
    option='1'
    while (option!='no'):
        item=input("Item :")
        if not(file2.check_menu(item)):
            print("The item is not in the menu")
            continue
        quantity=int(input("Quantity : "))
        orders[item]=quantity
        option=input("\nAdd more (yes,no) : ")
    option = input("Would you like to change something in the order? (yes/no): ").lower()
    if option == 'yes':
        change_order()
        print("Order changed.")
        display_order()
        cal=calculate_bill()
        order_no = random.randrange(0,999)
        print(f"\n{customer_name} Order no.={order_no}\n ")
        
    else:
        display_order()
        cal=calculate_bill()
        order_no = random.randrange(0,999)
        print(f"\n\n{customer_name}\n Order no.={order_no}\n ")
    file2.input_recipt(employee_id,customer_name,customer_no,cal)
    employee_choice()
#MAIN

time_now = int(dt.now().strftime("%H"))

if (time_now<3 or time_now>=9):
    print("Welcome to Restaurant\n\n")
    info()
else:
    print("the shop is close !!")


