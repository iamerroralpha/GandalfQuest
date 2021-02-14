import sqlite3
import pandas as pd
# Create your connection.
"""Easy to use, just use from importer import import_houses and then import_houses() returns the data contained in sqlite in a pandas df"""
def import_houses():
	cnx = sqlite3.connect('homes.db')
	df = pd.read_sql_query("SELECT * FROM houses", cnx)
	return(df)
