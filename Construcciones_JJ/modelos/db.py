import pymysql
pymysql.install_as_MySQLdb()

from flask_mysqldb import MySQL

db = MySQL()