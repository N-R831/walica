import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection
 
 
def _get_conn():
    """GSheetsConnectionを取得する"""
    return st.connection("gsheets", type=GSheetsConnection)
 
 
def _fetch_all():
    """walicaシートの全データを取得（キャッシュなし）"""
    conn = _get_conn()
    # カラム名は小文字で返ってくる
    df = conn.read(worksheet="walica", usecols=[0, 1, 2, 3, 4])
    # 空行を除去
    df = df.dropna(how="all")
    # カラム名を統一（小文字）
    df.columns = [c.lower() for c in df.columns]
    return df
 
 
def submit(member, date, kind, money):
    """新しいレコードを追加する"""
    conn = _get_conn()
    df = _fetch_all()
 
    # idの最大値を取得（データが空の場合は0から始める）
    if df.empty or "id" not in df.columns or df["id"].dropna().empty:
        max_id = 0
    else:
        max_id = int(df["id"].dropna().astype(int).max())
 
    df_append = pd.DataFrame({
        "id":     [max_id + 1],
        "date":   [date],
        "member": [member],
        "kind":   [kind],
        "money":  [int(money)],
    })
 
    df_update = pd.concat([df, df_append], ignore_index=True)
 
    conn.update(
        worksheet="walica",
        data=df_update,
    )
 
 
def read(str_sql):
    """SQL文でデータを取得する"""
    conn = _get_conn()
    # ttl=0でキャッシュを無効化し、常に最新データを返す
    df = conn.query(str_sql, ttl=0)
    # カラム名を小文字に統一
    df.columns = [c.lower() for c in df.columns]
    return df
 
 
def read_one_data(str_sql):
    """SQL文で単一の値を取得する"""
    conn = _get_conn()
    df = conn.query(str_sql, ttl=0)
    if df.empty:
        return None
    # 最初の行・最初のカラムの値を返す
    return df.iloc[0, 0]
 
 
def delete():
    """全データを削除する（シートを空にしてヘッダーだけ残す）"""
    conn = _get_conn()
    # ヘッダーだけの空DataFrameで上書き
    df_empty = pd.DataFrame(columns=["id", "date", "member", "kind", "money"])
    conn.update(
        worksheet="walica",
        data=df_empty,
    )
 
 
def delete_One_Data(id):
    """指定IDのレコードを削除する"""
    conn = _get_conn()
    df = _fetch_all()
 
    # 指定IDの行を除外（idカラムをint比較）
    df["id"] = df["id"].astype(int)
    df_ret = df[df["id"] != int(id)].reset_index(drop=True)
 
    conn.update(
        worksheet="walica",
        data=df_ret,
    )