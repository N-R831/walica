import streamlit as st
import calendar
from datetime import date 
import datetime
import sqlite3
import pandas as pd
from app import doSQL as dS
from streamlit_gsheets import GSheetsConnection

def get_month_range(year, month):
    """
    指定された年月の最初と最後の日付をタプルで返します。

    Args:
        year (int): 年
        month (int): 月

    Returns:
        tuple: (最初の日付, 最終日付)
    """
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    return first_day, last_day

st.title('My Walica')
# Sidebarの選択肢を定義する
options = ["金額入力", "結果", "詳細", "バックアップ"]
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
        dS.submit(member, str(d), kind, mon)
        st.cache_data.clear()
        st.rerun()
elif choice == "結果":
    today = datetime.date.today()
    year_now = today.year
    month_now = today.month
    min_day = dS.read('SELECT MIN(DATE) FROM "walica"')
    print(min_day['min(DATE)'][0])
    if len(min_day['min(DATE)'][0]) == 0:
        year_min = datetime.datetime.strptime(min_day[0], '%Y-%m-%d').year
    else:
        year_min = year_now
    options = [years for years in range(int(year_min), int(year_now)+1) ]
    if len(options) == 1:
        selected_year = st.text_input('年', year_now)
    else:
        selected_year = st.selectbox(
            '年',
            options,
            year_now
        )
    selected_month = st.selectbox(
        '年',
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', ],
        month_now-1
    )
    first_day, last_day = get_month_range(int(selected_year), int(selected_month))
    str_sql = 'SELECT DISTINCT(MEMBER) FROM "walica" WHERE MEMBER is NOT NULL'
    df_member = dS.read(str_sql)
    str_sql = f"""SELECT MEMBER, SUM(MONEY) FROM "walica" WHERE DATE BETWEEN '{first_day}' AND '{last_day}' GROUP BY MEMBER"""
    print(str_sql)
    df_ret = dS.read(str_sql)
    if not(df_ret.empty):
        for i in range(len(df_member)):
            print(df_member)
            if not(df_ret.empty):
                st.write(df_ret['member'][i], ":", df_ret['sum(MONEY)'][i])
            else:
                st.write(df_member['member'][i], ":", 0)
        str_sql = f"""SELECT SUM(MONEY) FROM "walica" WHERE MEMBER='花帆' AND
            DATE BETWEEN '{first_day}' AND '{last_day}' GROUP BY MEMBER"""
        kaho_money = dS.read(str_sql)
        str_sql = f"""SELECT SUM(MONEY) FROM "walica" WHERE MEMBER='涼馬' AND
            DATE BETWEEN '{first_day}' AND '{last_day}' GROUP BY MEMBER"""
        ryoma_money = dS.read(str_sql)
        print(kaho_money)
        if not(kaho_money.empty) and not(ryoma_money.empty):
            if kaho_money['sum(MONEY)'][0] > ryoma_money['sum(MONEY)'][0]:
                st.title("涼馬が花帆に" + str(int((kaho_money['sum(MONEY)'][0] - ryoma_money['sum(MONEY)'][0])/2)) + "円支払う" )
            elif ryoma_money['sum(MONEY)'][0] > kaho_money['sum(MONEY)'][0]:
                st.title("花帆が涼馬に" + str(int((ryoma_money['sum(MONEY)'][0] - kaho_money['sum(MONEY)'][0])/2)) + "円支払う" )
            else:
                st.title("どちらも支払う必要はありません")
elif choice == "詳細":
    today = datetime.date.today()
    year_now = today.year
    month_now = today.month
    min_day_df = dS.read('SELECT MIN(DATE) FROM "walica"')
    print(min_day_df)
    min_day = min_day_df['min(DATE)'][0]
    if len(min_day) == 0:
        year_min = datetime.datetime.strptime(min_day[0], '%Y-%m-%d').year
    else:
        year_min = year_now
    
    options = [years for years in range(int(year_min), int(year_now)+1) ]
    
    print(len(options))
    if len(options) == 1:
        selected_year = st.text_input('年', year_now)
    else:
        selected_year = st.selectbox(
            '年',
            options,
            year_now
        )
    selected_month = st.selectbox(
        '年',
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', ],
        month_now-1
    )
    
    first_day, last_day = get_month_range(int(selected_year), int(selected_month))
    str_sql = f"""SELECT * FROM "walica" WHERE DATE BETWEEN '{first_day}' AND '{last_day}'"""
    print("ここ" + str_sql)
    df = dS.read(str_sql)
    selected_row = st.dataframe(data=df)
    text_id = st.text_input('id', '')
    if st.button('削除'):
        dS.delete_One_Data(text_id)
        st.success("削除しました")
        st.cache_data.clear()
        st.rerun()

elif choice == "バックアップ":
    str_sql = f'SELECT * FROM "walica"'
    df = dS.read(str_sql)
    st.dataframe(df)

    # CSVファイルのアップロード
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])
    # アップロードされたファイルをデータフレームに読み込む
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        print(df)
        if st.button('復旧'):
            print("復旧します")
            rows = len(df)
            dS.delete()
            for row in range(0, rows):
                print(rows)
                member = df['member'][row]
                d = df['date'][row]
                kind = df['kind'][row]
                mon = df['money'][row]
                print(member)
                print(d)
                print(kind)
                print(mon)
                dS.submit(member, str(d), kind, int(mon))
            st.success("復旧しました")
            st.cache_data.clear()
            st.rerun()
else:
    st.write("Errror")
    

