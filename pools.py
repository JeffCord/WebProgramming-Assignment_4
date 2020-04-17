import os
import time

from flask import request
from flask import Flask, render_template
import mysql.connector
from mysql.connector import errorcode
import json

application = Flask(__name__)
app = application


def get_db_creds():
    db = os.environ.get("DB", None) or os.environ.get("database", None)
    username = os.environ.get("USER", None) or os.environ.get("username", None)
    password = os.environ.get("PASSWORD", None) or os.environ.get("password", None)
    hostname = os.environ.get("HOST", None) or os.environ.get("dbhost", None)
    return db, username, password, hostname


def create_table():
    # Check if table exists or not. Create and populate it only if it does not exist.
    db, username, password, hostname = get_db_creds()
    table_ddl = 'CREATE TABLE pools(pool_name VARCHAR(100) NOT NULL, status VARCHAR(13), phone VARCHAR(12), ' \
                'pool_type VARCHAR(12), PRIMARY KEY (pool_name))'

    cnx = ''
    try:
        # sets up a connection with the mysql server
        cnx = mysql.connector.connect(user=username, password=password, host=hostname, database=db)
    except Exception as exp:
        print(exp)

    # Create an object that can execute operations such as SQL statements.
    # Cursor objects interact with the MySQL server using a MySQLConnection object.
    cur = cnx.cursor()

    try:
        cur.execute(table_ddl)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg, '$$$')


@app.route("/static/add_pool", methods=['POST'])
def add_pool():

    # Assignment 4: Insert Pool into database.
    # Extract all the form fields
    pool_name = request.form['pool_name']
    status = request.form['status']
    print("Pool Name:" + pool_name)
    print("Status:" + status)

    # Insert into database.
    return render_template('pool_added.html')


@app.route("/pools", methods=['GET'])  # TODO ask about adding this GET method header check
def get_pools():
    db, username, password, hostname = get_db_creds()

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
    except Exception as exp:
        print(exp)

    check_cur = cnx.cursor()
    check_cur.execute('SELECT * FROM pools_data.pools')
    my_result = check_cur.fetchall()
    print(my_result)

    return render_template('pools.html')


@app.route("/")
def pool_info_website():
    return render_template('index.html')  # renders the html file to be displayed in the browser


# # validations for the fields of each pool
# def validate_status(s):
#     valid_statuses = ['Closed', 'Open', 'In Renovation']
#     return s in valid_statuses
#
#
# def validate_pool_types(s):
#     valid_pool_types = ['Neighborhood', 'University', 'Community']
#     return s in valid_pool_types
#
#
# def validate_phone(s):
#     if len(s) != 10:
#         return False
#
#     for i in s:
#         if not i.isdigit():
#             return False
#
#     return True


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')