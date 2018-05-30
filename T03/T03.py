import sqlite3
import csv

dic = {"Bruno": "Lertora", "Enzo": "Zambon", "Jose": "Oniate", "Erick": "Moncada", "Juan": "Gonzalez"}

file = open('users.csv', 'w')

columnTitleRow = "Username, Password\n"
file.write(columnTitleRow)

for key in dic.keys():
    username = key
    password = dic[key]
    row = username + "," + password + "\n"
    file.write(row)

file = open('listened_tracks.csv', 'w')

columnTitleRow = "Username, Time\n"
file.write(columnTitleRow)

file.write( + "," +  + "\n")



# connection = sqlite3.connect('AC9.csv')
# cursor = connection.cursor()
# cursor.execute("CREATE TABLE clientes(id TEXT, nombre TEXT, apellido TEXT, rut TEXT, pais TEXT)")
# cursor.execute("CREATE TABLE transferencias(transID TEXT, clientID TEXT, monto INTEGER)")
# cursor.execute("INSERT INTO clientes VALUES ('00001', 'Bruno', 'Lertora', '19087952-2', 'Chile')")
# cursor.execute("INSERT INTO clientes VALUES ('00002', 'Enzo', 'Zambon', '18723152-8', 'Zambia')")
# cursor.execute("INSERT INTO clientes VALUES ('00003', 'Jose', 'Oñate', '20560152-3', 'Iquique')")
# cursor.execute("INSERT INTO clientes VALUES ('00004', 'Erick', 'Moncada', '19960152-9', 'Chile')")
# cursor.execute("INSERT INTO clientes VALUES ('00005', 'Juan', 'Perez', '18992352-5', 'Chile')")
#
# cursor.execute("INSERT INTO transferencias VALUES ('0001', '00001', '20000')")
# cursor.execute("INSERT INTO transferencias VALUES ('0010', '00002', '15000')")
# cursor.execute("INSERT INTO transferencias VALUES ('0011', '00003', '25000')")
# cursor.execute("INSERT INTO transferencias VALUES ('0100', '00004', '10000')")
# cursor.execute("INSERT INTO transferencias VALUES ('0101', '00005', '30000')")
#
# connection.commit()
#
# connection = sqlite3.connect('AC09.db')
# cursor = connection.cursor()
# cursor.execute('SELECT C.nombre, C.apellido, C.rut FROM clientes C')
# print(cursor.fetchall())
# cursor.execute('SELECT DISTINCT C.nombre FROM clientes C')
# print(cursor.fetchall())
# cursor.execute('SELECT T.transID FROM transferencias T WHERE T.monto > 5000')
# print(cursor.fetchall())
# cursor.execute('SELECT C.nombre, C.apellido, C.rut FROM clientes C WHERE C.nombre = "Patricio" OR "Felipe"')
# print(cursor.fetchall())
# cursor.execute('SELECT C.nombre, C.apellido, C.rut FROM clientes C WHERE (C.nombre = "Patricio" OR "Felipe") '
#                'AND C.pais != "Hanslandia"')
# print(cursor.fetchall())
# cursor.execute('SELECT C.nombre, C.apellido, C.rut FROM clientes C WHERE (C.nombre = "Patricio" OR "Felipe") '
#                'AND C.pais != "Hanslandia" ORDER BY C.rut')
# print(cursor.fetchall())
# cursor.execute("INSERT INTO clientes VALUES ('00001', 'Bruno', 'Lertora', '19087952-2', 'Chile')")
# print(cursor.fetchall())
# cursor.execute("UPDATE clientes SET pais = 'Hanslandia' WHERE clientid = '00001'")
# print(cursor.fetchall())
# cursor.execute("DELETE FROM clientes WHERE clientid = '00001'")
# print(cursor.fetchall())
# cursor.execute('SELECT MAX (T.monto) FROM transferencias T UNION SELECT MIN (T.monto) FROM transferencias T')
# print(cursor.fetchall())
# cursor.execute('SELECT MAX (T.monto), MIN (T.monto) FROM transferencias T, Clientes C WHERE T.clientid = C.clientid and'
#                ' C.nombre = "Bastian"')
# print(cursor.fetchall())
# cursor.execute('SELECT C.nombre, C.apellido, T.transid, T.clientid, T.monto FROM transferencias T, Clientes C WHERE '
#                'T.clientid = C.clientid')
# print(cursor.fetchall())
#
# connection.commit()
# connection.close()
#
#
