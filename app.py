#!/Users/purinatpat/miniforge3/bin/python
# -*- coding: utf-8
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
import credential # Manually done

app = Flask(__name__)

app.config['MYSQL_HOST'] = credential._mysql_host
app.config['MYSQL_USER'] = credential._mysql_user
app.config['MYSQL_PASSWORD'] = credential._mysql_password
app.config['MYSQL_DB'] = credential._mysql_db
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # Dictionary

mysql = MySQL(app)

# Home page
@app.route('/')
def index():
    # Flask looks inside the templates folder
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'crypto_test'
    app.run(debug=True)