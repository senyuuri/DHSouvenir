# db_create.py
import sqlite3
from config import DATABASE_PATH
with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()
    '''
    c.execute("""CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, passwd TEXT NOT NULL)""")
    c.execute("""CREATE TABLE uorder(user_id INTEGER, olist BLOB)""")
    c.execute("""CREATE TABLE store(id INTEGER, name TEXT, price REAL, num INTEGER)""")
    storelist = [
    			(0,"A4 lecture pad", 2.60, 100),
				(1,"7-colour sticky note with pen", 4.20, 100),
				(2,"A5 ring book", 4.80, 100),
				(3,"A5 note book with zip bag", 4.60, 100) ,
				(4,"2B pencil", 0.90, 100),
				(5,"Stainless steel tumbler", 12.90, 100),
				(6,"A4 clear holder", 4.40, 100),
				(7,"A4 vanguard file", 1.00, 100),
				(8,"Name card holder", 10.90, 100),
				(9,"Umbrella", 9.00, 100),
				(10,"School badge (Junior High)", 1.30, 100),
				(11,"School badge (Senior High)", 1.80, 100),
				(12,"Dunman dolls (pair))", 45.00, 100),
    ]
    c.executemany("""INSERT INTO store VALUES (?,?,?,?) """, storelist)
    connection.commit()
    '''
    c.execute("""ALTER TABLE user ADD COLUMN email TEXT""")
  