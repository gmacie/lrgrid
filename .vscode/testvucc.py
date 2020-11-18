import pyodbc, csv

drivers = [x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
#print(drivers)

try:
    con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\DXLab\DXKeeper\Databases\N4LR.mdb;'    
    conn = pyodbc.connect(con_string)
    print("Connected to Database")
except pyodbc.Error as e:
    print("Error in Connection",e)

cursor = conn.cursor()
sql = "select GRID, MIXED, M6 from VUCCProgress"
cursor.execute(sql)
res = cursor.fetchall()

with open("dxlab_vucc.csv","w") as file:
    for row in res:
        csv.writer(file).writerow(row)

cursor.close()