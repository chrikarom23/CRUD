import sqlite3

def dbcheck():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY,name text, password text)")
    cur.execute("CREATE TABLE IF NOT EXISTS Items (name text UNIQUE, price float)")
    conn.commit()
    conn.close()
