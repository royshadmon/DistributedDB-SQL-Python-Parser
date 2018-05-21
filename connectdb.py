# https://www.fullstackpython.com/blog/postgresql-python-3-psycopg2-ubuntu-1604.html
# https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
import psycopg2

class runDB(object):
    def __init__(self, query): 
        self.query = query

    def selectStmt(self):
        try:
            connect_str = "dbname='royshadmon' user='royshadmon' host='localhost' " + \
                            "password=''"
            # use our connection values to establish a connection
            conn = psycopg2.connect(connect_str)
            # create a psycopg2 cursor that can execute queries
            cursor = conn.cursor()
            #cursor.execute(query)
            cursor.execute(self.query)
            rows = cursor.fetchall()
            print(rows)
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
