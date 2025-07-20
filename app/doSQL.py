import streamlit as st
from streamlit_gsheets import GSheetsConnection
import datetime
import pandas as pd
import os

def sumit(member, date, kind, money):
    # データベース(GoogleSpreadSheet)に接続
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_check = conn.query('SELECT max(id) FROM "kakeibo" ')
    id = df['id']
    if df_check.empty:
        id = 1
    else: 
        id = id + 1
    df_append = pd.DataFrame({'id': [id], '日付': [date], 'メンバー': [member], '名目': [kind], '金額': [money]})
    df = conn.update(
        worksheet="kakeibo",
        data=df_append,
    )
    st.cache_data.clear()
    st.rerun()
    
