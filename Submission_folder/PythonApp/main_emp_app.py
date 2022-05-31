import py_app_DB as pya
import pymysql
from time import strptime
import pickle
from datetime import datetime
import calendar

arr = []

# main function. Calls main menu. redirects each of the choices.
def main():
    
    while True:
        display_menu()
        choice = input("Enter choice: ")
		
        if choice == "1":
            viewEandD()
        
        elif choice == "2":
            salary()
        
        elif choice == "3":
            month()
                  
        elif choice == "4":
            addNew()

        elif choice == "5":
            viewDept()
        
        elif choice == "6":
            addManager()

        elif choice == "7":            
            arr.append(choice)
            if len(arr) < 2:
                viewAll()
            else:
                viewAll2()
        
        elif choice == "8":
            avgs()

        elif choice == "x":
            break
        
        else:
            print("==============================")
            print("***Invalid entry*** Try again!")
            print("==============================")

# Option 1	- view employee name and department in groups of 2		
def viewEandD():
    choice1 = ""
    offset = 0
    counter = 2   
    while choice1 != "q":  
        # calls appropriate function in py_app_DB.py module      
        x = pya.optionOne()
        # chooses only the rows dictated by offset/counter values
        x = x[offset:counter]
        print("------------------")
        # prints table headings each view
        print("Name  | Department") 
        print("------------------")
        for i in x:
            print(i["employee"], " | ", i["dept"])
        print("------------------")
        choice1 = input("press any key to view the next two employees, or 'q' to quit: ")
        # increase offset and counter values to view next 2 employees
        if choice1 != "q":
            offset  += 2
            counter += 2   
        # quits and return to main menu                 
        elif choice1 == "q":
            continue

# Option 2 - returns minimum, average and maximum salary details for employee
def salary():
    # takes user input for Employee ID
    ID = input("Enter Employee ID (e.g. E01): ")
    try:
        # calls appropriate function in py_app_DB.py module 
        x = pya.optionTwo(ID)        
        print("\nSalary details for Employee: ", ID)
        print("-----------------------------------")
        print("Minimum     | Average     | Maximum     ")
        print("-----------------------------------")
        for i in x:
            print(i["Minimum"] + "   | " + i["Average"] + "   | " + i["Maximum"])
        print("-----------------------------------")
    # if non existant EID is entered nothing is displayed except table headings
    except: 
        print("")

# Option 3 - to view employees born in a particular month inputted by user
def month():
    while True:
        month = input("Enter Month (e.g. 3 or Mar): ")
        # checks if input is numeric
        if month.isnumeric():
            # converts user unput from string to integer
            month = int(month)
            # month number obviously has to be less than 13
            if month < 13:
                try:
                    # calls appropriate function in py_app_DB.py module
                    x = pya.optionThree(month)
                    # uses calendar function to convert number to full text month
                    print("\nEmployees born in", calendar.month_name[month])                    
                    print("---------------------------------")
                    print("EID | Name        | Date of Birth")
                    print("---------------------------------")
                    for i in x:
                        print(i["eid"], " |", i["name"], " |", i["dob"])
                    print("---------------------------------")
                    break
                except: 
                    print("")
            else:
                if month > 12:
                    print("=====================")
                    print("**ERROR** Invalid month entered") 
                    print("=====================")  
        # if input is text             
        else:
            try:
                # 'try' 'strptime()' function with '%b' to convert 3 letter input to 
                # numeric representation of month
                monthNumber = strptime(month, '%b').tm_mon
                try:
                    print("\nEmployees born in", calendar.month_name[monthNumber])
                    print("---------------------------------")
                    print("EID | Name        | Date of Birth")
                    print("---------------------------------")
                    # calls appropriate function in py_app_DB.py module
                    x = pya.optionThree(monthNumber)
                    for i in x:
                        print(i["eid"], " |", i["name"], " |", i["dob"])
                    print("---------------------------------")
                    break
                except: 
                    print("")
            # if strptime() didn't work
            except:
                print("==============================")
                print("**ERROR** Invalid month format \nEnter month number or first 3 letters, i.e. 3 or Mar")
                print("==============================")

# Option 4 - function to add new employee
def addNew():
    eid = input("Enter Employee ID (e.g. E01): ")
    name = input("Enter Employee name: ")
    dob = input("Enter Employee date of birth (format: yyyy-mm-dd): ")
    did = input("Enter Employee Department ID (e.g. PROD1): ")        
    # calls appropriate function in py_app_DB.py module
    x = pya.optionFour(eid, name, dob, did)
    # if employee input is successful
    if x == True:
        print("\nNew employee successfully added")
        print("==================================================")
        print("EID: " + eid + " | NAME: " + name + " | DOB: " + dob + " | DID: " + did)
        print("==================================================")

# Option 5 - function to view department managed by employee and its budget
def viewDept():
    x = input("ENTER EID: ")
    # calls appropriate function in py_app_DB.py module
    y = pya.optionFive1(x)
    if y:
        print("\nDepartment(s) managed by: ", x)
        print("--------------------------")
        print("Department | Budget")
        print("--------------------------")
        for i in y:
            print(i["did"], "    | ", i["budget"])
        print("--------------------------")
        print("")

# Option 6 - function to create management relationship between employee and department
def addManager():
    eid = input("Enter EID : ")
    did = input("Enter DID : ")
    pya.optionSix1(eid, did)

# Option 7
def viewAll():
    newA = []
    x = pya.optionSeven()
    print("\nDid  | Department | Location | Budget")  
    print("=======================================")  
    for i in x:
        print(i["did"], " | ", i["name"], " | ", i["lid"], " | ", i["budget"])

# Option 7 still
def viewAll2():
    # reads file from 'pickle' file stored in memory
    with open('file.pkl', 'rb') as f:
        x = pickle.load(f)
        print("\nDid  | Department | Location | Budget")
        print("=======================================")
        for i in x:
            print(i["did"], " | ", i["name"], " | ", i["lid"], " | ", i["budget"])

# Option 8 (innovation!)
def avgs():
    print("\nChoose one of the following options:")
    print("------------------------------------")
    print ("1 - Current ages of employees by department: ")
    print ("2 - Max salary by department: ")
    print("3 - Table of average age and current employee average salary: ")
    choice = input("Enter: ")
    if choice == "1":
        choice2 = input("Enter Department ID: ")
        x = pya.optionEightA(choice2)
        print("\nCurrent ages of employees in the", choice2, "department")
        print("-----------------")
        print("Name        | Age")
        print("-----------------")
        for i in x:
            print(i['name'], " | ", i['Age'])
        print("-----------------")
    elif choice == "2":
        choice2 = input("Enter Department ID: ")
        y = pya.optionEightB(choice2)
        print("--------------------------------------------------------------")
        for j in y:
            print("The current maximum salary in the", choice2, "department is:", j['MAX'])
        print("--------------------------------------------------------------")
    elif choice == "3":
        z = pya.optionEightC()
        print("\nAVG EMP age | AVG Current salary | Dept name")
        print("------------------------------------------------------------")
        for k in z:
            print("    ", k["avg_age"], "    |   ", k["AVG_MAX"], "   | ", k["dept_name"])
        print("------------------------------------------------------------")
    else:
        print("==========================")
        print("***ERROR*** Invalid entry!")
        print("==========================")

def display_menu():
    print("\n -----------")
    print("| Employees |")
    print(" -----------")
    print("  MAIN MENU")
    print("  =========")
    print ("1 - View Employees & Departments")
    print ("2 - View Salary Details")
    print ("3 - View by Month of Birth")
    print ("4 - Add New Employee")
    print ("5 - View Departments managed by Employee")
    print ("6 - Add Manager to Department")
    print ("7 - View Departments")
    print ("8 - Further age and salary data")
    print ("x - Exit application")


if __name__ == "__main__":
    main()