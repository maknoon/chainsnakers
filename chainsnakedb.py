#!~/usr/bin/python3

import pymysql

# Open database connection
db = PyMySQL.connect("localhost","testuser","test123","TESTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# Create table as per requirement
term_table_query = """CREATE TABLE TERM (
   T_ID  INT AUTO_INCREMENT PRIMARY_KEY,
   T_NAME  VARCHAR(32),
   T_DESCP VARCHAR(256) )"""

cursor.execute(term_table_query)

label_table_query = """CREATE TABLE LABEL (
	L_ID INT AUTO_INCREMENT PRIMARY_KEY,
	L_NAME VARCHAR(32) )"""

cursor.execute(label_table_query)

relationship_table_query = """CREATE TABLE TERM (
	R_ID INT,
	L_ID INT,
	T_ID INT,
	CONSTRAINT PK_RELATIONSHIP PRIMARY_KEY (L_ID, T_ID),
	CONSTRAINT FK_LABEL
		FOREIGN KEY (L_ID) REFERENCES LABEL (L_ID),
	CONSTRAINT FK_TERM
		FOREIGN KEY (T_ID) REFERENCES TERM (T_ID),
	 )"""

# disconnect from server
db.close()