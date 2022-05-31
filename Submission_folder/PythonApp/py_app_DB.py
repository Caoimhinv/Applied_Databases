import pymysql
from neo4j import GraphDatabase
from neo4j import exceptions
import pickle

driver = None
conn = None

# function to connect to mysql database
def connect():
    global conn
    conn = pymysql.connect(host="localhost",
                            user = "root",
                            password="root",
                            db="employees",
                            cursorclass=pymysql.cursors.DictCursor)

# function to connect to neo4j database
def connect4():
    global driver
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"), max_connection_lifetime=1000)

# function to view employee name and department
def optionOne():
    connect()
    query = """
                SELECT e.name AS employee, d.name AS dept 
                FROM employee e 
                JOIN dept d ON e.did = d.did 
                ORDER BY d.name, e.name
                """
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        value = cursor.fetchall()        
        return value

# function to view min, max, and avg salary        
def optionTwo(eid):    
    connect()
    query = """
                SELECT FORMAT(MIN(salary),2) AS Minimum, FORMAT(AVG(salary), 2) AS Average, 
                FORMAT(MAX(salary),2) AS Maximum 
                FROM salary WHERE eid = %s
                """
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, (eid))
        x = cursor.fetchall()
        return x

# function to view employees born in a month entered by user
def optionThree(monthNum):
    connect()
    query = "SELECT eid, name, dob FROM employee WHERE month(dob) = %s"
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, (monthNum))
        x = cursor.fetchall()
        return x       
 
# function to create new employee 
def optionFour(x,y,z,v):
    connect()   
    query = "INSERT INTO employee VALUES (%s, %s, %s, %s)"
    with conn:
        try:
            cursor = conn.cursor()
            x = cursor.execute(query, (x,y,z,v))
            conn.commit()
            return(x)
        # exceptions
        except pymysql.IntegrityError as e:     
            if e.args[0] == 1062:
                print("=================================================")
                print("***ERROR***: Employee ID **", x,"** already exists")
                print("=================================================")
            else:
                # if Department ID doesn't exist
                if e.args[0] == 1452:
                    print("==========================================")
                    print("***ERROR***: Department", v,"does not exist")
                    print("==========================================")
        except pymysql.err.OperationalError as e:
            # invalid date format
            if e.args[0] == 1292:
                print("================================================================================")
                print("***ERROR***: Invalid DOB! You entered:", z, "- format should be yyyy-mm-dd")
                print("================================================================================")
        except Exception as e:
            # too many characters entered for either EID or DID
            if e.args[0] == 1406:
                print("===========================================================================")
                print("***ERROR***: Invalid entry for EID/Department. Too many characters entered!")
                print("===========================================================================")
            else:
                # all other exceptions
                print("================================================")
                print("***ERROR***: ", e)
                print("================================================")

# functions to return departments and budgets managed by employee
def optionFive(tx, y):
    # returns all departments managed by employee
    query = "MATCH(e:Employee{eid:$module})-[m:MANAGES]->(d) RETURN d.did"
    emps = []
    results = tx.run(query, module=y)
    for result in results:
        emps.append(result["d.did"])
    # returns list of department IDs
    return emps

def optionFive1(x):
    connect4()
    with driver.session() as session:
        # gets result from function 'optionfive()' above
        y = session.read_transaction(optionFive, x) 
        # if no results are returned     
        if len(y) == 0:
            print("\nDepartment(s) managed by: ", x)
            print("--------------------------")
            print("Department | Budget")
            print("--------------------------\n")           
        else:
            query1 = "SELECT did, format(budget, 0) AS budget FROM dept WHERE did = %s"
            query2 = "SELECT did, format(budget, 0) AS budget FROM dept WHERE did = %s OR did = %s"
            query3 = "SELECT did, format(budget, 0) AS budget FROM dept WHERE did = %s OR did = %s  OR did = %s"
            query3 = "SELECT did, format(budget, 0) AS budget FROM dept WHERE did = %s OR did = %s  OR did = %s OR did = %s"
            connect()
            with conn:
                cursor = conn.cursor()
                # depending on length of list returned
                if len(y) == 1:
                    cursor.execute(query1, (y[0]))
                    x = cursor.fetchall()
                elif len(y) == 2:
                    cursor.execute(query2, (y[0], y[1]))
                    x = cursor.fetchall()
                elif len(y) == 3:
                    cursor.execute(query3, (y[0], y[1], y[2]))
                    x = cursor.fetchall()
                elif len(y) == 4:
                    cursor.execute(query4, (y[0], y[1], y[2], y[3]))
                    x = cursor.fetchall()
                return x

# function to insert employee managing a department                
def optionSix(tx, eid, did):
    query2 = """
                MERGE (e:Employee{eid:$eid}) 
                CREATE (d:Department{did:$did}) 
                MERGE (e)-[m:MANAGES]->(d) 
                RETURN e, m, d
                 """
    tx.run(query2, eid=eid, did=did)

# function to create unique constraint on did if it doesn't exist already
def optionSix2(tx):
    query1 = """
                CREATE CONSTRAINT constraint_DID IF NOT EXISTS FOR (d:Department) 
                REQUIRE d.did IS UNIQUE
                """
    tx.run(query1)

# function to check if eid and did are in sql database. And if create 'manages' relationship
# and insert whatever necessary in neo4j database
def optionSix1(eid,did):
    # first checks whether eid and did are in the sql database
    connect()
    query1 = "SELECT * FROM employee WHERE eid = %s"
    query2 = "SELECT * FROM dept WHERE did = %s"
    with conn:
        cursor = conn.cursor()
        cursor.execute(query1, (eid))
        value = cursor.fetchall()  
        if not value:
            print("-=======================================")
            print("***ERROR*** Employee:", eid, "does not exist")
            print("-=======================================")          
        else:
            connect()
            with conn:
                cursor = conn.cursor()
                cursor.execute(query2, (did))
                value = cursor.fetchall()         
                if not value:
                    print("-=========================================")
                    print("***ERROR*** Department:", did, "does not exist") 
                    print("-=========================================")          
                else:
                    # if 'eid' and 'did' are in the sql database we continue and attempt to
                    # create the relationship in the neo4j database
                    try:
                        connect4()
                        # creates a unique constraint on 'did' if not there already
                        with driver.session() as session:         
                            values = session.write_transaction(optionSix2)
                        # tries to create the relationship
                        with driver.session() as session:         
                            values = session.write_transaction(optionSix, eid, did)
                            print("----------------------------------------------")
                            print("Employee: ", eid, " now manages Department: ", did)
                            print("----------------------------------------------")
                    # if the 'did' unique constraint is violated we get the following error
                    except exceptions.ConstraintError:
                        print("-===============================================") 
                        print("***ERROR*** Department:", did, "already has a manager")
                        print("-===============================================") 

# function to retrieve all dept info from sql database and save to file
def optionSeven():
    connect()
    query = "SELECT * FROM dept"
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    # write the python 'dict' to file using pickle module
    f = open("file.pkl","wb")
    pickle.dump(results,f)
    f.close()
    return results

# function to select current ages of employees in a department
def optionEightA(x):
    connect()
    query = """
                SELECT name, ROUND(datediff(now(), dob) / 365.25) AS Age
                FROM employee WHERE did = %s;
                """
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, (x))
        results = cursor.fetchall()
    return results

# function to select maximum salary of employees per department
def optionEightB(y):
    connect()
    query = """
                SELECT FORMAT(MAX(s.salary),2) as MAX 
                FROM salary s JOIN employee e ON s.eid = e.eid 
                WHERE e.did = %s
                """
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, (y))
        results = cursor.fetchall()
    return results

# function to select dept name, avg age, and AVG current salary per department
def optionEightC():
    connect()
    query = """
               SELECT d.did, d.name AS dept_name, ROUND(AVG(datediff(now(), dob) / 365.25)) as avg_age, 
                FORMAT(AVG(maxSal),2) AS AVG_MAX FROM (
                SELECT s.eid, MAX(s.salary) AS maxSal FROM salary s 
                GROUP BY s.eid) as s
                RIGHT JOIN employee e ON s.eid = e.eid 
                JOIN dept d ON e.did = d.did
                GROUP BY d.did
                ORDER BY AVG_MAX DESC;
                """
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    return results