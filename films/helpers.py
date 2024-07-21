import os
import sqlite3
import dotenv
import jwt

con = sqlite3.connect("spoooooook.sqlite")
cur = con.cursor()

dotenv.load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")


def selectQueryDB(query: str, values: str, isFetchAll: bool) -> list | tuple:
    results: sqlite3.Cursor = cur.execute(query, values)

    if isFetchAll:
        return results.fetchall()
    else:
        return results.fetchone()


def validateJWT(token):

    try:
        jwt.decode(token, key=JWT_SECRET, algorithms=['HS256'])
        return True
    except Exception:
        return False
