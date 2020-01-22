import sqlite3
from sqlite3 import Error

database = 'todo.db'
def createConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established")
        createTable(conn)
    except Error as e:
        print(e)
    return conn

# Create table
def createTable(conn):
    try:
        c = conn.cursor()
        query = """ CREATE TABLE IF NOT EXISTS notes(dt DATE, id INT PRIMARY KEY, title TEXT, desc TEXT, status TEXT NOT NULL, priority TEXT); """
        c.execute(query)
        print("Table creation successful !")
    except Error as e:
        print(e)

# Display rows
def displayRows():
    try:
        conn = createConnection(database)
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM notes; """)
        rows = cur.fetchall()
        return { "count": len(rows), "items": rows }
    except Exception as e:
        print('Error: ', e)
        return None

# Display row based on Id
def displayRowBasedOnId(values):
    try:
        conn = createConnection(database)
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM notes WHERE id = ?; """,(values,))
        row = cur.fetchone()
        return { "item": row }
    except Exception as e:
        print('Error: ', e)
        return None


# Insert new note
def addNotes(item):
    conn = createConnection(database)
    cur = conn.cursor()
    cur.execute("INSERT INTO notes(dt,id,title,desc,status,priority) VALUES(?,?,?,?,?,?);",
            (item['dt'],item['id'],item['title'],item['desc'],item['status'],item['priority']))
    conn.commit()
    
    return { "Date" : item['dt'],
             "Title": item['title'],
             "Desc" : item['desc'],
             "Status": item['status'],
             "Priority":item['priority'] }

# Update Status / Priority based on Opt
def updateNotes(opt, values):
    conn = createConnection(database)
    cur = conn.cursor()
    if opt == "status" :
        query = """ UPDATE notes SET status = ? WHERE id = ? ;"""
    elif opt == "priority":
        query = """ UPDATE notes SET priority = ? WHERE id = ? ; """
    cur.execute(query, values)
    conn.commit()
    get_query = """ SELECT * from notes WHERE id = ?; """
    cur.execute(get_query,(values[1],))
    row = cur.fetchone()
    return { "item" : row }

# Clear all notes
def deleteAll():
    conn = createConnection(database)
    cur = conn.cursor()
    query = """ DELETE FROM notes;"""
    cur.execute(query)
    conn.commit()

# Clear a note based on Id 
def deleteNotes(values):
    conn = createConnection(database)
    cur = conn.cursor()
    query = """ DELETE FROM notes WHERE id = ? ;"""
    cur.execute(query,(values,))
    conn.commit()
    cur.execute(""" SELECT * FROM notes; """)
    rows = cur.fetchall()
    return { "count": len(rows), "items": rows }


if __name__ == '__main__':
    main()
