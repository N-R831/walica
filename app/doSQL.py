import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection
 
 
def _get_conn():
    """GSheetsConnectionを取得する"""
    return st.connection(
        "gsheets",
        type=GSheetsConnection,
        spreadsheet="https://docs.google.com/spreadsheets/d/1FnLva6GbMA4xBs_JowC8Uq0A7aCSXtBnXVIEOLIlSmk"
    )
 
 
def _fetch_all():
    """walicaシートの全データを取得"""
    conn = _get_conn()
    df = conn.read(worksheet="walica", usecols=[0, 1, 2, 3, 4], ttl=0)
    df = df.dropna(how="all")
    df.columns = [c.lower() for c in df.columns]
    # 空文字列・NaNのid行を除去
    df = df[df["id"].notna()]
    df = df[df["id"].astype(str).str.strip() != ""]
    return df
 
 
def submit(member, date, kind, money):
    """新しいレコードを追加する"""
    conn = _get_conn()
    df = _fetch_all()
 
    if df.empty or "id" not in df.columns or df["id"].dropna().empty:
        max_id = 0
    else:
        max_id = int(pd.to_numeric(df["id"], errors="coerce").dropna().max())
 
    df_append = pd.DataFrame({
        "id":     [max_id + 1],
        "date":   [str(date)],
        "member": [member],
        "kind":   [kind],
        "money":  [int(money)],
    })
 
    df_update = pd.concat([df, df_append], ignore_index=True)
    conn.update(worksheet="walica", data=df_update)
 
 
def read(str_sql):
    """
    SQL文を解釈してPython側でフィルタリングして返す。
    conn.query()の代替実装。
    """
    df = _fetch_all()
 
    if df.empty:
        return df
 
    sql = str_sql.strip().lower()
 
    # MIN(date) クエリ
    if "min(date)" in sql:
        min_val = df["date"].min() if not df["date"].dropna().empty else ""
        return pd.DataFrame({"min(date)": [str(min_val)]})
 
    # DISTINCT(member) クエリ
    if "distinct" in sql and "member" in sql:
        members = df["member"].dropna().unique()
        return pd.DataFrame({"member": list(members)})
 
    # date BETWEEN フィルタ
    if "between" in sql:
        import re
        m = re.search(r"between\s+'([^']+)'\s+and\s+'([^']+)'", sql)
        if m:
            date_from = m.group(1)
            date_to = m.group(2)
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
            date_from_d = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to_d = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
            df = df[(df["date"] >= date_from_d) & (df["date"] <= date_to_d)]
 
    # member = 'X' フィルタ
    if "member=" in sql.replace(" ", ""):
        import re
        m = re.search(r"member\s*=\s*'([^']+)'", str_sql)
        if m:
            target_member = m.group(1)
            df = df[df["member"] == target_member]
 
    # GROUP BY member + SUM(money)
    if "group by member" in sql and "sum(money)" in sql:
        df["money"] = pd.to_numeric(df["money"], errors="coerce").fillna(0)
        df = df.groupby("member", as_index=False)["money"].sum()
        df.columns = ["member", "sum(money)"]
        return df.reset_index(drop=True)
 
    # SUM(money) のみ（GROUP BYなし）
    if "sum(money)" in sql and "group by" not in sql:
        df["money"] = pd.to_numeric(df["money"], errors="coerce").fillna(0)
        total = df["money"].sum()
        return pd.DataFrame({"sum(money)": [total]})
 
    # SELECT * など
    df["money"] = pd.to_numeric(df["money"], errors="coerce").fillna(0)
    return df.reset_index(drop=True)
 
 
def read_one_data(str_sql):
    """単一の値を取得する"""
    df = read(str_sql)
    if df is None or df.empty:
        return None
    return df.iloc[0, 0]
 
 
def delete():
    """全データを削除する（ヘッダーだけ残す）"""
    conn = _get_conn()
    df_empty = pd.DataFrame(columns=["id", "date", "member", "kind", "money"])
    conn.update(worksheet="walica", data=df_empty)
 
 
def delete_One_Data(id):
    """指定IDのレコードを削除する"""
    conn = _get_conn()
    df = _fetch_all()
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df_ret = df[df["id"] != int(id)].reset_index(drop=True)
    conn.update(worksheet="walica", data=df_ret)