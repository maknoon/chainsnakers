#!~/usr/bin/python

import pymysql as psql
import config

class ChainsDb(object):

    def __init__(self):
        return

    def reset_db(self):
        # Open database connection
        db = psql.connect(config.host,config.dbusr,config.dbpwd,"chains" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # Drop table if it already exist using execute() method.
        cursor.execute("DROP TABLE IF EXISTS RELATIONSHIPS, C_KW_RELATIONSHIPS, KEY_WORDS, TOPIC, CARD;")

        # Create table as per requirement
        term_table_query = """CREATE TABLE KEY_WORDS (
           K_ID INT AUTO_INCREMENT PRIMARY KEY,
           K_NAME VARCHAR(32));"""

        cursor.execute(term_table_query)

        label_table_query = """CREATE TABLE TOPIC (
            T_ID INT AUTO_INCREMENT PRIMARY KEY,
            T_NAME VARCHAR(32));"""

        cursor.execute(label_table_query)

        relationship_table_query = """CREATE TABLE RELATIONSHIPS (
            K_ID INT,
            T_ID INT,
            R_WEIGHT DOUBLE,
            CONSTRAINT PK_RELATIONSHIP PRIMARY KEY (T_ID, K_ID),
            CONSTRAINT FK_TOPIC
                FOREIGN KEY (T_ID) REFERENCES TOPIC (T_ID),
            CONSTRAINT FK_KEY_WORDS
                FOREIGN KEY (K_ID) REFERENCES KEY_WORDS (K_ID)
             );"""

        cursor.execute(relationship_table_query)

        card_table_query = """CREATE TABLE CARD (
            C_ID INT AUTO_INCREMENT PRIMARY KEY,
            K_ID INT,
            C_QUESTION VARCHAR(256),
            C_ANSWER VARCHAR(256)
            );"""

        cursor.execute(card_table_query)

        c_kw_relationship_table_query = """CREATE TABLE C_KW_RELATIONSHIPS (
            K_ID INT,
            C_ID INT,
            CONSTRAINT PK_C_KW_RELATIONSHIP PRIMARY KEY (C_ID, K_ID),
            CONSTRAINT FK_CARD
                FOREIGN KEY (C_ID) REFERENCES CARD (C_ID),
            CONSTRAINT FK_WORDS
                FOREIGN KEY (K_ID) REFERENCES KEY_WORDS (K_ID)
            );"""

        cursor.execute(c_kw_relationship_table_query)


        # disconnect from server
        db.close()

        # if __name__ == '__main__':
        #     reset_db()

    def insert_to_topics(self, name):
        # Open database connection
        db = psql.connect(config.host,config.dbusr,config.dbpwd,"chains" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        insert_query = """INSERT INTO TOPIC (
                            T_NAME ) VALUES (
                            '%s')""" % (name)
        cursor.execute(insert_query)
        db.commit()
        # disconnect from server
        db.close()

    def insert_to_key_word(self, name):
        # Open database connection
        db = psql.connect(config.host,config.dbusr,config.dbpwd,"chains" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        insert_query = """INSERT INTO KEY_WORDS (
                            K_NAME ) VALUES (
                            '%s')""" % (name)
        cursor.execute(insert_query)
        db.commit()
        # disconnect from server
        db.close()

    def insert_to_relationships(self, kname, tname, weight):
        # Open database connection
        db = psql.connect(config.host,config.dbusr,config.dbpwd,"chains" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        k_select_query = """SELECT K_ID FROM KEY_WORDS
                             WHERE K_NAME =
                            '%s'""" % (kname)
        cursor.execute(k_select_query)
        data = cursor.fetchone()
        k_id = data[0]

        t_select_query = """SELECT T_ID FROM TOPIC
                             WHERE T_NAME =
                            '%s'""" % (tname)
        cursor.execute(t_select_query)
        data = cursor.fetchone()
        t_id = data[0]

        r_insert_query = """INSERT INTO RELATIONSHIPS (
                              K_ID, T_ID, R_WEIGHT) VALUES (
                              %d, %d, %f)""" % (k_id, t_id, weight)
        cursor.execute(r_insert_query)
        db.commit()

        # disconnect from server
        db.close()




chainsDb = ChainsDb()
chainsDb.reset_db()
chainsDb.insert_to_topics("SOLAR SYSTEMS")
chainsDb.insert_to_key_word("cell barrier")
chainsDb.insert_to_relationships("cell barrier", "SOLAR SYSTEMS", 0.22)
print "meow"