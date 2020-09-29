import mysql.connector
import pandas as pd

try:
    con=mysql.connector.connect(user='root', password='pihul', host='localhost', port=3306, database='sakila')
    if con.is_connected():
        print('Connected to Database!')
        ### Show databases available

        sql1="desc film"
        cur=con.cursor()
        cur.execute(sql1)
        lst_cols=cur.column_names
        fp = open("desc_table.csv", "w")
        for i in lst_cols:
            header=str(i) + ':'
            fp.write(header)
            print(header, end=" ")
        fp.write("\n")
        print("")


        row=cur.fetchall()

        for i in row:
            for j in i:
                record=str(j) +  ':'
                fp.write(record)
                print(record,end=" ")
            fp.write("\n")
            print("")



        df=pd.read_csv('desc_table.csv',sep=":")
        print(df)






except Exception as e:
    print('Unable to connect to database....',e)
finally:
    fp.close()
    cur.close()
    con.close()