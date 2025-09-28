import streamlit as st
import sqlite3
import datetime
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection


dbname = 'MASTER.db'

# データベース(GoogleSpreadSheet)に接続
conn = st.connection("gsheets", type=GSheetsConnection)

def submit(member, date, kind, money):
    # db接続
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.query('SELECT id, date, member, kind, money, FROM "walica" WHERE date is NOT NULL ORDER BY id DESC')
    print(df['id'].max())
    max_id = df['id'].max()
    df_append = pd.DataFrame({'id': [max_id+1], 'date': [date], 'member': [member], 'kind': [kind], 'money': [money], })
    df_update = pd.concat([df, df_append])
    df = conn.update(
        worksheet="walica",
        data=df_update,
    )
    

def read(str_sql):
    # db接続
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.query(str_sql)
    return df

def read_one_data(str_sql):
    # db接続
    conn = st.connection("gsheets", type=GSheetsConnection)
    print(str_sql)
    df = conn.query(str_sql)
    print(df)
    ret = df[0][0]
    
    return ret

def delete():
    # db接続
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    conn.execute('DELETE FROM "walica"')
    conn.commit()

    conn.close()

def delete_One_Data(id):
    # db接続
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.query('SELECT id, date, member, kind, money, FROM "walica" WHERE date is NOT NULL ORDER BY id ASC')
    print("do")
    for i in range(len(df['id'])):
        if int(df['id'][i]) == int(id):
            print(df)
            df_ret = df.drop(i)
            print(df)
    df_ret = conn.update(
                    worksheet="walica",
                    data=df_ret,
                )
    

    
