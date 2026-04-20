import streamlit as st
import calendar
from datetime import date
import datetime
import pandas as pd
from app import doSQL as dS
<<<<<<< HEAD
 
 
=======
from streamlit_gsheets import GSheetsConnection

>>>>>>> d26eb3194947a455eb0f5182d42d5903154a811c
def get_month_range(year, month):
    """指定された年月の最初と最後の日付をタプルで返す"""
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    return first_day, last_day
 
 
st.title('My Walica')
<<<<<<< HEAD
 
=======
>>>>>>> d26eb3194947a455eb0f5182d42d5903154a811c
# Sidebarの選択肢を定義する
options = ["金額入力", "結果", "詳細", "バックアップ"]
choice = st.sidebar.selectbox("メニュー", options)
 
 
# ── 金額入力 ──────────────────────────────────────────
if choice == "金額入力":
    member = st.selectbox('支払った人', ['涼馬', '花帆'])
    d = st.date_input('支払日', datetime.datetime.today())
    kind = st.text_input('名目', '')
    mon = st.text_input('金額', '')
 
    if st.button('登録'):
<<<<<<< HEAD
        if kind == '' or mon == '':
            st.warning("名目と金額を入力してください")
        else:
            dS.submit(member, str(d), kind, mon)
            st.cache_data.clear()
            st.success("登録しました")
            st.rerun()
 
 
# ── 結果 ──────────────────────────────────────────────
=======
        dS.submit(member, str(d), kind, mon)
        st.cache_data.clear()
        st.rerun()
>>>>>>> d26eb3194947a455eb0f5182d42d5903154a811c
elif choice == "結果":
    today = datetime.date.today()
    year_now = today.year
    month_now = today.month
<<<<<<< HEAD
 
    min_day_df = dS.read('SELECT MIN(date) FROM "walica"')
    # カラム名は小文字: 'min(date)'
    min_day_col = min_day_df.columns[0]
    min_day_val = min_day_df[min_day_col].iloc[0]
 
    if pd.isna(min_day_val) or str(min_day_val) == '':
=======
    min_day = dS.read('SELECT MIN(DATE) FROM "walica"')
    print(min_day['min(DATE)'][0])
    if len(min_day['min(DATE)'][0]) == 0:
        year_min = datetime.datetime.strptime(min_day[0], '%Y-%m-%d').year
    else:
>>>>>>> d26eb3194947a455eb0f5182d42d5903154a811c
        year_min = year_now
    else:
        year_min = datetime.datetime.strptime(str(min_day_val), '%Y-%m-%d').year
 
    year_options = list(range(int(year_min), int(year_now) + 1))
 
    if len(year_options) == 1:
        selected_year = year_now
        st.text(f'年: {selected_year}')
    else:
        selected_year = st.selectbox('年', year_options, index=len(year_options) - 1)
 
    selected_month = st.selectbox(
        '月',
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        index=month_now - 1
    )
 
    first_day, last_day = get_month_range(int(selected_year), int(selected_month))
<<<<<<< HEAD
 
    str_sql = f"""SELECT member, SUM(money) as total FROM "walica"
        WHERE date BETWEEN '{first_day}' AND '{last_day}' GROUP BY member"""
    df_ret = dS.read(str_sql)
 
    if not df_ret.empty:
        for _, row in df_ret.iterrows():
            st.write(f"{row['member']} : {int(row['total'])} 円")
 
        # 花帆・涼馬それぞれの合計
        kaho_row = df_ret[df_ret['member'] == '花帆']
        ryoma_row = df_ret[df_ret['member'] == '涼馬']
 
        kaho_total = int(kaho_row['total'].iloc[0]) if not kaho_row.empty else 0
        ryoma_total = int(ryoma_row['total'].iloc[0]) if not ryoma_row.empty else 0
 
        diff = abs(kaho_total - ryoma_total) // 2
 
        if kaho_total > ryoma_total:
            st.title(f"涼馬が花帆に {diff} 円支払う")
        elif ryoma_total > kaho_total:
            st.title(f"花帆が涼馬に {diff} 円支払う")
        else:
            st.title("どちらも支払う必要はありません")
    else:
        st.info("この月のデータはありません")
 
 
# ── 詳細 ──────────────────────────────────────────────
=======
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
>>>>>>> d26eb3194947a455eb0f5182d42d5903154a811c
elif choice == "詳細":
    today = datetime.date.today()
    year_now = today.year
    month_now = today.month
<<<<<<< HEAD
 
    min_day_df = dS.read('SELECT MIN(date) FROM "walica"')
    min_day_col = min_day_df.columns[0]
    min_day_val = min_day_df[min_day_col].iloc[0]
 
    if pd.isna(min_day_val) or str(min_day_val) == '':
=======
    min_day_df = dS.read('SELECT MIN(DATE) FROM "walica"')
    print(min_day_df)
    min_day = min_day_df['min(DATE)'][0]
    if len(min_day) == 0:
        year_min = datetime.datetime.strptime(min_day[0], '%Y-%m-%d').year
    else:
>>>>>>> d26eb3194947a455eb0f5182d42d5903154a811c
        year_min = year_now
    else:
        year_min = datetime.datetime.strptime(str(min_day_val), '%Y-%m-%d').year
 
    year_options = list(range(int(year_min), int(year_now) + 1))
 
    if len(year_options) == 1:
        selected_year = year_now
        st.text(f'年: {selected_year}')
    else:
        selected_year = st.selectbox('年', year_options, index=len(year_options) - 1)
 
    selected_month = st.selectbox(
        '月',
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        index=month_now - 1
    )
 
    first_day, last_day = get_month_range(int(selected_year), int(selected_month))
<<<<<<< HEAD
 
    str_sql = f"""SELECT * FROM "walica" WHERE date BETWEEN '{first_day}' AND '{last_day}'"""
    df = dS.read(str_sql)
    st.dataframe(data=df)
 
    text_id = st.text_input('削除するID', '')
    if st.button('削除'):
        if text_id == '':
            st.warning("IDを入力してください")
        else:
            dS.delete_One_Data(text_id)
            st.success("削除しました")
            st.cache_data.clear()
            st.rerun()
 
 
# ── バックアップ ───────────────────────────────────────
elif choice == "バックアップ":
    str_sql = 'SELECT * FROM "walica"'
=======
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
>>>>>>> d26eb3194947a455eb0f5182d42d5903154a811c
    df = dS.read(str_sql)
    st.dataframe(df)
 
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])
    if uploaded_file is not None:
        df_csv = pd.read_csv(uploaded_file)
        st.dataframe(df_csv)
        if st.button('復旧'):
            dS.delete()
            for _, row in df_csv.iterrows():
                dS.submit(
                    str(row['member']),
                    str(row['date']),
                    str(row['kind']),
                    int(row['money'])
                )
            st.success("復旧しました")
            st.cache_data.clear()
            st.rerun()
 
else:
    st.write("Error")