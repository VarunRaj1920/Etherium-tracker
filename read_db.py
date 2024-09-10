# read data from sqlite db "eth_deposit.db"

import sqlite3

def main():
    con = sqlite3.connect('eth_deposit.db')
    cur = con.cursor()

    print("Deposit table schema:")
    print()
    cur.execute("PRAGMA table_info(deposit)")
    row = cur.fetchone()
    print(row)
    print()
    cur.execute("SELECT * FROM deposit")
    rows = cur.fetchall()
    print("All deposits:")
    print()
    for row in rows:
        print(row)
    con.close()

if "__main__" == __name__:
    main()