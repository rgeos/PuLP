#!/usr/bin/env python

DEBUG = True
LOG_LEVEL = 'DEBUG'
SECRET_KEY = 'hard_to_guess'

db_postgres = 'postgresql://user:pass@localhost:5432/db'
# db_mysql = 'mysql://user:pass@localhost:3306/db'
db_sqlite = 'sqlite:///../data/US_elections_2016.sqlite'

SQLALCHEMY_DATABASE_URI = db_sqlite

SQLALCHEMY_BINDS = {
	'sqlite': db_sqlite,
	# 'mysql': db_mysql,
	'postgres': db_postgres
}
SQLALCHEMY_TRACK_MODIFICATIONS = False


