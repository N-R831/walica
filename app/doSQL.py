import streamlit as st
import sqlite3
import datetime
import pandas as pd
import os


dbname = 'MASTER.db'

# テーブルを作成する 
conn = sqlite3.connect(dbname)
conn.execute('''
CREATE TABLE IF NOT EXISTS master_dt ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    date TEXT NOT NULL,
    member TEXT NOT NULL,
    kind TEXT NOT NULL,
    money INTEGER NOT NULL
) 
''')

def submit(member, date, kind, money):
    # db接続
    conn = sqlite3.connect(dbname)
    
    conn.execute("INSERT INTO master_dt (date, member, kind, money) VALUES (?, ?, ?, ?)", (date, member, kind, money))
    conn.commit()

    conn.close()

def read(str_sql):
    # db接続
    conn = sqlite3.connect(dbname)
    df = pd.read_sql_query(str_sql, conn)
    conn.close()
    return df

def read_one_data(str_sql):
    # db接続
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    print(str_sql)
    cur.execute(str_sql)
    ret = cur.fetchall()

    cur.close()
    conn.close()
    
    return ret[0]

def delete():
    # db接続
    conn = sqlite3.connect(dbname)
    
    conn.execute("DELETE FROM master_dt")
    conn.commit()

    conn.close()

def delete_One_Data(id):
    # db接続
    conn = sqlite3.connect(dbname)
    str_sql=f"DELETE FROM master_dt WHERE id ={id}"
    print(str_sql)
    conn.execute(str_sql)
    conn.commit()

    conn.close()
    
