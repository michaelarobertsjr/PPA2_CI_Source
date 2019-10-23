from flask import Flask
from importlib import reload
import ppa2src as functions
import sqlalchemy
import pymysql
import datetime

reload(functions)
#Web Service
ppa2_app = Flask(__name__)

@ppa2_app.route('/bmi')
def bmi_all():
    
    connection = functions.connect_db()
    previousBMIs = connection.execute('SELECT * FROM bmi').fetchall()
    
    return 'Previous BMIs:\n ' + str(previousBMIs)

@ppa2_app.route('/distance')
def distance_all():

    connection = functions.connect_db()
    previousDistances = connection.execute('SELECT * FROM distance').fetchall()

    return 'Previous Distances:\n' + str(previousDistances)

@ppa2_app.route('/bmi/<string:combined_height>/<int:weight>')
def bmi(combined_height, weight):
    connection = functions.connect_db()

    split_height = combined_height[:1] + ' ' + combined_height[1:]
    newBMI = functions.calcBMI(split_height, weight)
    
    save_string = 'INSERT INTO bmi VALUES (\'' + str(split_height) + '\', ' + str(weight) + ', \'' + str(newBMI) + '\', \'' + str(datetime.datetime.now()) + '\')'
    connection.execute(save_string)

    out_string = 'New BMI: %s \n' % newBMI
    return out_string

@ppa2_app.route('/distance/<int:x1>/<int:y1>/<int:x2>/<int:y2>')
def distance(x1, y1, x2, y2):
    connection = functions.connect_db()

    newDistance = functions.calcDistance(x1, y1, x2, y2)

    save_string = 'INSERT INTO distance VALUES(\'' + str(x1) + '\', \'' + str(y1) + '\', \'' + str(x2) + '\', \'' + str(y2) + '\', ' + str(newDistance) + ', \'' + str(datetime.datetime.now()) + '\')'
    connection.execute(save_string)

    out_string = 'New Distance: %s \n' % str(newDistance)
    return out_string

if __name__ == '__main__':
    #Web Service start
    ppa2_app.run()
