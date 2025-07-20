import streamlit as st
import  datetime
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from app import doSQL as dS


st.title('My Walica')


# Sidebarの選択肢を定義する
options = ["金額入力", "結果", "詳細"]
choice = st.sidebar.selectbox("メニュー", options)

# Mainコンテンツの表示を変える
if choice == "金額入力":
    member = st.selectbox(
        '支払った人', 
        ['涼馬', '花帆',]
    )
    # テキスト入力ボックス
    d = st.date_input('支払日', datetime.datetime.today())
    kind = text_input = st.text_input('名目', '')
    mon = text_input = st.text_input('金額', '')
    if st.button('登録'):
        dS.sumit(member, str(d), kind, mon)
elif choice == "結果":
    st.write("You selected Option 2")
elif choice == "詳細":
    st.write("You selected Option 3")
else:
    st.write("Errror")