# import mysql.connector
#
# try:
#     con=mysql.connector.connect(user='root', password='pihul', host='localhost', port=3306, database='sakila')
#     if con.is_connected():
#         print('Connected to Database!')
#         ### Show databases available
#
#         sql1='SELECT * FROM `actor`'
#         cur=con.cursor()
#         cur.execute(sql1)
#         cur.fetchall()
#         rc=cur.rowcount
#         print(rc)
#
#
# except Exception as e:
#     print('Unable to connect to database....',e)
# finally:
#     cur.close()
#     con.close()

import mysql.connector

try:
    con=mysql.connector.connect(user='root', password='pihul', host='localhost', port=3306, database='sakila')
    if con.is_connected():
        print('Connected to Database!')
        ### Show databases available

        sql1='DESC `film`'
        cur=con.cursor()
        cur.execute(sql1)
        data_cur=cur
        cur.fetchall()
        rc = cur.rowcount
        print(rc)
        print(data_cur)

        for d in data_cur:
            print("hello")
            print(d)








except Exception as e:
    print('Unable to connect to database....',e)
finally:
    cur.close()
    con.close()