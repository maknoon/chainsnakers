#!~/usr/bin/python

import pymysql as psql
import config
<<<<<<< 7f982c0e034d21a7474937900a4b62c4696e8eb1

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
            C_QUESTION VARCHAR(256),
            C_ANSWER VARCHAR(256)
            );"""

        cursor.execute(card_table_query)

        c_kw_relationship_table_query = """CREATE TABLE C_KW_RELATIONSHIPS (
            K_ID INT,
            C_ID INT,
            WEIGHT DOUBLE,
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

    def insert_to_card(self, question, answer):
        # Open database connection
        db = psql.connect(config.host,config.dbusr,config.dbpwd,"chains" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        insert_query = """INSERT INTO CARD (
                            C_QUESTION, C_ANSWER ) VALUES (
                            '%s', '%s')""" % (question, answer)

        cursor.execute(insert_query)
        db.commit()

        db.close()

    def insert_to_c_kw(self, question, word, weight):
        # Open database connection
        db = psql.connect(config.host,config.dbusr,config.dbpwd,"chains" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        q_select_query = """SELECT C_ID FROM CARD
                             WHERE C_QUESTION =
                            '%s'""" % (question)
        cursor.execute(q_select_query)
        data = cursor.fetchone()
        c_id = data[0]

        w_select_query = """SELECT K_ID FROM KEY_WORDS
                             WHERE K_NAME =
                            '%s'""" % (word)
        cursor.execute(w_select_query)
        data = cursor.fetchone()
        w_id = data[0]

        c_kw_insert_query = """INSERT INTO C_KW_RELATIONSHIPS (
                              C_ID, K_ID, WEIGHT) VALUES (
                              %d, %d, %f)""" % (c_id, w_id, weight)
        cursor.execute(c_kw_insert_query)
        db.commit()

        # disconnect from server
        db.close()

    def get_questions_given_keyword(self, word):
        # Open database connection
        db = psql.connect(config.host,config.dbusr,config.dbpwd,"chains" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        k_select_query = """SELECT K_ID FROM KEY_WORDS
                             WHERE K_NAME =
                            '%s'""" % (word)
        cursor.execute(k_select_query)
        data = cursor.fetchone()
        try:
            k_id = data[0]
        except:
            db.close()
            return {}

        q_select_query = """SELECT CARD.C_QUESTION FROM CARD 
                             INNER JOIN C_KW_RELATIONSHIPS
                             ON CARD.C_ID = C_KW_RELATIONSHIPS.C_ID
                             INNER JOIN KEY_WORDS
                             ON C_KW_RELATIONSHIPS.K_ID = KEY_WORDS.K_ID
                             WHERE C_KW_RELATIONSHIPS.WEIGHT > 0.7 AND C_KW_RELATIONSHIPS.K_ID = %i
                             ORDER BY C_KW_RELATIONSHIPS.WEIGHT DESC LIMIT 3;""" % (k_id)

        cursor.execute(q_select_query)
        data = cursor.fetchall()

        try:
            if data[0] is not None: questions = data
        except:
            questions = {}

        i = 0
        array = []
        while i < len(questions):
            array.append(questions[i][0])
            i += 1
        
        # disconnect from server
        db.close()

        return {"questions":array}

    def get_keyword_given_question(self, question):
        # Open database connection
        db = psql.connect(config.host,config.dbusr,config.dbpwd,"chains" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        q_select_query = """SELECT C_ID FROM CARD
                             WHERE C_QUESTION =
                            '%s'""" % (question)
        cursor.execute(q_select_query)
        data = cursor.fetchone()
        try:
            c_id = data[0]
        except:
            db.close()
            return {}

        k_select_query = """SELECT KEY_WORDS.K_NAME FROM KEY_WORDS 
                             INNER JOIN C_KW_RELATIONSHIPS
                             ON KEY_WORDS.K_ID = C_KW_RELATIONSHIPS.K_ID
                             INNER JOIN CARD
                             ON C_KW_RELATIONSHIPS.C_ID = CARD.C_ID
                             WHERE C_KW_RELATIONSHIPS.WEIGHT > 0.7 AND C_KW_RELATIONSHIPS.C_ID = %i
                             ORDER BY C_KW_RELATIONSHIPS.WEIGHT DESC LIMIT 3;""" % (c_id)

        cursor.execute(k_select_query)
        data = cursor.fetchall()

        try:
            if data[0] is not None: words = data
        except:
            words = {}
        
        i = 0
        array = []
        while i < len(words):
            array.append(words[i][0])
            i += 1

        # disconnect from server
        db.close()
        return {"words":array}

chainsDb = ChainsDb()
chainsDb.reset_db()
chainsDb.insert_to_topics("SOLAR SYSTEMS")
chainsDb.insert_to_key_word("cell barrier")
chainsDb.insert_to_key_word("woofers")
chainsDb.insert_to_relationships("cell barrier", "SOLAR SYSTEMS", 0.22)
chainsDb.insert_to_card("How old is trent really?", "probably like forty years old")
chainsDb.insert_to_card("How sexy are you?", "very very very sexy")
chainsDb.insert_to_c_kw("How old is trent really?", "cell barrier", 0.891)
chainsDb.insert_to_c_kw("How sexy are you?", "cell barrier", 0.701)
chainsDb.insert_to_c_kw("How old is trent really?", "woofers", 0.791)
print chainsDb.get_questions_given_keyword("cell barrier")
print chainsDb.get_keyword_given_question("How old is trent really?")
print "meow"