import sqlite3 

##connectiong to sqlite
connection=sqlite3.connect("student.db")

#create cursor for inserting data 
cursor=connection.cursor()

#Create table 
table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)

##Insert some more records
cursor.execute('''Insert Into STUDENT values('Varun','ECE','G2',90) ''')
cursor.execute('''Insert Into STUDENT values('Urvi','DS','G2',95) ''')
cursor.execute('''Insert Into STUDENT values('Abhi','DS','G1',68) ''')
cursor.execute('''Insert Into STUDENT values('Yashi','Arts','G1','87') ''')
cursor.execute('''Insert Into STUDENT values('Aryan','COM','G7',89) ''')
cursor.execute('''Insert Into STUDENT values('Ani','Neet','G2',75) ''')

##DIsplay all the records
print("The inserted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

#Commit changes database

connection.commit()
connection.close()