import sqlite3

con = sqlite3.connect("spoooooook.sqlite")
cur = con.cursor()

def selectQueryDB(query, values, isFetchAll):
    results = cur.execute(query, values)

    if isFetchAll:
        return results.fetchall()
    else:
        return results.fetchone()

