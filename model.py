##############################################################
#
# File :- Model.py
#
#Description :- This file saves the data to the DB for analysis
#
#Author :- Team Fantastic4
#
###############################################################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)

DATABASE = 'tripplanner'
PASSWORD = 'cloud123'
USER = 'clouduser'
HOSTNAME = 'aws.cbmuqc9mcupo.us-east-1.rds.amazonaws.com'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate_obj = Migrate(app, db)
manager_obj = Manager(app)

manager_obj.add_command('db', MigrateCommand)

class TripResult(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sourcelocation = db.Column(db.String(1000))
    destinations = db.Column(db.String(10000))
    uberprice = db.Column(db.String(100))
    lyftprice = db.Column(db.String(100))
    optimalprice = db.Column(db.String(100))
    bestprovider = db.Column(db.String(100))


    def __init__(self, sourcelocation, destinations, uberprice, lyftprice, optimalprice, bestprovider):
        self.sourcelocation = sourcelocation
        self.destinations = destinations
        self.uberprice = uberprice
        self.lyftprice = lyftprice
        self.optimalprice = optimalprice
        self.bestprovider = bestprovider


def createdb():
    import sqlalchemy
    engine = sqlalchemy.create_engine('mysql://%s:%s@%s'%(USER, PASSWORD, HOSTNAME)) # connect to server
    engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE)) #create db

if __name__ == '__main__':
	manager_obj.run()



