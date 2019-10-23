import math, datetime
import sqlalchemy as db
import pymysql
import ppa2web
import subprocess as sp
from importlib import reload

#Connect to ppa2_values database
def connect_db():
    db_config = {
        'host' : '192.168.99.100',
        'port' : '32769',
        'user' : 'root',
        'pass' : 'roots',
        'db' : 'ppa2_values'
    }

    access_str = 'mysql+pymysql://%s:%s@%s:%s/%s' % (db_config['user'], db_config['pass'], '192.168.99.100', db_config['port'], db_config['db'])
    engine = db.create_engine(access_str, pool_pre_ping=True)
    conn = engine.connect()

    return conn

#Switch connecting the function menu to the internal functions
def chooseFunction(x, conn):

    myFunctions = {'1' : getBMI, '2' : getRetirement, '3' : getDistance, '4' : getEmail }

    chosenFunction = myFunctions.get(x, lambda : print('Please input a number 1 - 4 to use a function or 5 to exit...\n'))

    if x == 1:

        bmi_values = conn.execute('SELECT input_height, input_weight, output_stats, timestamp FROM bmi').fetchall()
        print('BMI:\ninput_height, input_weight, output_stats, timestamp\n')
        for n in bmi_values:
            print(str(n) + '\n')

    elif x == 3:

        distance_values = conn.execute('SELECT input_x1, input_y1, input_x2, input_y2, output_distance, timestamp FROM distance').fetchall()
        print('Distance:\ninput_x1, input_y1, input_x2, input_y2, output_distance, timestamp\n')
        for m in distance_values:
            print(str(m) + '\n')

    output = chosenFunction(conn)
    print(output)  

#BMI Categorizer I/O
def getBMI(db_conn):

    height_sep = input('Please enter your height in feet and inches separated by a space (e.g. 5 7 for 5 feet 7 inches)\n')

    weight = input('Please enter your weight in pounds\n')

    result = calcBMI(height_sep, weight)
    save_string = 'INSERT INTO bmi VALUES (\'' + str(height_sep) + '\', ' + weight + ', \'' + str(result) + '\', \'' + str(datetime.datetime.now()) + '\')'
    db_conn.execute(save_string)

    return(result)
 
#BMI Categorizer calculation
def calcBMI(ht, wt):

    height_in = (float(ht.split()[0]) * 12) + float(ht.split()[1])
    height_m = height_in * 0.025
    weight_kg = float(wt) * 0.45

    bmi = weight_kg / (height_m ** 2)

    stats = 'Value: ' + str(bmi) + ' Category: '

    if bmi <= 18.5:
        stats += 'Underweight'
    elif bmi > 18.5 and bmi <= 24.9:
        stats += 'Normal Weight'
    elif bmi > 24.9 and bmi <= 29.9:
        stats += 'Overweight'
    elif bmi >= 29.9:
        stats += 'Obese'

    stats += '\n'
    return stats

#Retirement Estimator I/O
def getRetirement(db_conn):

    age = input('Please enter your current age\n')
    salary = input('Please enter your current annual salary\n')
    saveRate = input('Please enter the percentage of your annual salary that you save yearly\n')
    saveGoal = input('Please enter your retirement savings goal\n')

    return(calcRetirement(age, salary, saveRate, saveGoal))

#Retirement Estimator calculation
def calcRetirement(currentAge, currentSalary, percentSave, goalSave):

    yearsNeeded = int(float(goalSave) / (float(currentSalary) * float(percentSave) * 0.01 * 1.35))
    retirementAge = int(currentAge) + int(yearsNeeded)

    if retirementAge < 100:
        return 'Your savings goal will be met at age ' + str(retirementAge)
    else:
        return 'Unortunately, your savings goal was too ambitious'

#Distance Calculator I/O
def getDistance(db_conn):

    x1 = input('Please enter the x coordinate for the first point\n')
    y1 = input('Please enter the y coordinate for the first point\n')
    x2 = input('Please enter the x coordinate for the second point\n')
    y2 = input('Please enter the y coordinate for the second point\n')

    result = calcDistance(x1, y1, x2, y2)
    save_string = 'INSERT INTO distance VALUES(\'' + str(x1) + '\', \'' + str(y1) + '\', \'' + str(x2) + '\', \'' + str(y2) + '\', ' + str(result) + ', \'' + str(datetime.datetime.now()) + '\')'
    db_conn.execute(save_string)

    return('Distance: ' + str(result) + '\n')

#Distance Calculator calculation
def calcDistance(xOne, yOne, xTwo, yTwo):

    sum1 = (float(xTwo) - float(xOne))**2
    sum2 = (float(yTwo) - float(yOne))**2

    distance = math.sqrt(sum1 + sum2)

    return distance

#Email Verifier I/O
def getEmail(db_conn):

    email = input('Please enter your email address\n')

    return(verifyEmail(email))

#Email Verifier calculation
def verifyEmail(address):

    illegalCharacters = ['(', ')', ':', ';', '<', '>', ',', '[', ']']
    validation = 'This email address is '

    temp = 'valid!'
    count = 0
    if address[0] == '.' or address[len(address) - 1] == '.':
        temp = 'invalid'
    elif '..' in address:
        temp =  'invalid'
    else:
        for char in address:
            if char in illegalCharacters:
                temp = 'invalid'
            if char == '@':
                count += 1
    if count != 1:
        temp = 'invalid'
    validation += temp

    return validation

#Main loop that handles the function menu and program exit
def start(conn):
    condition = True
    while condition:

        available = ['1', '2', '3', '4', '5']

        choice = input('''
            Please select a function to execute...

            1. Determine BMI
            2. Estimate Retirement Age
            3. Calculate Distance
            4. Verify Email
            5. Exit

            ''')  
        if choice in available:
            if choice == '5':
                condition = False
                conn.close()
            else:
                chooseFunction(choice, conn)


if __name__ == '__main__':
    #Database Connection
    initial_conn = connect_db()
    initial_conn.execute('CREATE DATABASE IF NOT EXISTS ppa2_values')
    initial_conn.execute('CREATE TABLE IF NOT EXISTS bmi(input_height VARCHAR(10), input_weight INT, output_stats VARCHAR(50), time_run datetime)')
    initial_conn.execute('CREATE TABLE IF NOT EXISTS distance(input_x1 INT, input_y1 INT, input_x2 INT, input_y2 INT, output_distance VARCHAR(50), time_run datetime)')

    #Web Interface
    reload(ppa2web)
    web_server = sp.Popen('ppa2web.py', shell=True)

    try:
        #Database Connection
        a = initial_conn.execute('SELECT input_height, input_weight, output_stats, timestamp FROM bmi').fetchall()
        b = initial_conn.execute('SELECT input_x1, input_y1, input_x2, input_y2, output_distance, timestamp FROM distance').fetchall()

        print('Values after Last Program Execution:\n')
        print('BMI:\ninput_height, input_weight, output_stats, timestamp\n')
        for entry in a:
            print(str(entry) + '\n')
        print('Distance:\ninput_x1, input_y1, input_x2, input_y2, output_distance, timestamp\n')
        for item in b:
            print(str(item) + '\n')

        start(initial_conn)
        web_server.terminate()
    except EOFError as error:
        print(error)   