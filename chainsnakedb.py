#!~/usr/bin/python

import pymysql as psql
import config

# print config.host
# print config.dbusr

# Open database connection
db = psql.connect(config.host,config.dbusr,config.dbpwd,"chains" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS RELATIONSHIPS, TERM, LABEL;")

# Create table as per requirement
term_table_query = """CREATE TABLE TERM (
   T_ID INT AUTO_INCREMENT PRIMARY KEY,
   T_NAME VARCHAR(32),
   T_DESCP VARCHAR(256));"""

cursor.execute(term_table_query)

label_table_query = """CREATE TABLE LABEL (
	L_ID INT AUTO_INCREMENT PRIMARY KEY,
	L_NAME VARCHAR(32));"""

cursor.execute(label_table_query)

relationship_table_query = """CREATE TABLE RELATIONSHIPS (
	R_ID INT,
	L_ID INT,
	T_ID INT,
	CONSTRAINT PK_RELATIONSHIP PRIMARY KEY (L_ID, T_ID),
	CONSTRAINT FK_LABEL
		FOREIGN KEY (L_ID) REFERENCES LABEL (L_ID),
	CONSTRAINT FK_TERM
		FOREIGN KEY (T_ID) REFERENCES TERM (T_ID)
	 );"""

cursor.execute(relationship_table_query)

# disconnect from server
db.close()