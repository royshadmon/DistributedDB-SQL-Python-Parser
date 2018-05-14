# https://www.fullstackpython.com/blog/postgresql-python-3-psycopg2-ubuntu-1604.html
# https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
import psycopg2

try:
    connect_str = "dbname='royshadmon' user='royshadmon' host='localhost' " + \
                  "password=''"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    #cursor.execute("""CREATE TABLE tutorials (name char(40));""")
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("""SELECT * from turbine;""")
    rows = cursor.fetchall()
    print(rows)
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)
