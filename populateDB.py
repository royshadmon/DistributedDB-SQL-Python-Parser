# https://www.fullstackpython.com/blog/postgresql-python-3-psycopg2-ubuntu-1604.html
# https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
import psycopg2


def stmt():
    try:
        connect_str = "dbname='royshadmon' user='royshadmon' host='localhost' " + \
                            "password=''"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        query = "Create Table If Not Exists Turbine ( Temperature Int, Pressure Int, EventTime Date );"
        cursor.execute(query)
        conn.commit()
        query = "Insert Into Turbine Values (80, 5, '2018-04-23'), (82, 7, '2018-03-13'),  (89, 12, '2017-01-15'),  (60, 12, '2018-02-17'),  (102, 20, '2018-01-21'),  (82, 7, '2018-03-16'),  (81, 4,'2018-03-13'),  (62, 9, '2018-03-13');"
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

if __name__ == "__main__":
    stmt()
