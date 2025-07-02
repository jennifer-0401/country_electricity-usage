import pandas as pd
import streamlit as st
import numpy as np
df = pd.read_csv('2017_-_Electricity__heat__steam_and_cooling_purchased_for_local_government_consumption_20250702.csv')

#data preprocessing

# 標準化能源單位為 kWh
df['Amount_kWh'] = df.apply(
    lambda row: row['Amount'] * 1000 if row['Units'] == 'MWh' else row['Amount'],
    axis=1
)

# 按 Type 分組並加總
type_summary = df.groupby('Type')['Amount_kWh'].sum().reset_index()

# -- streamlit app -- #
st.set_page_config(
    page_title="國家地方政府能源消耗分析",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("🌍 國家地方政府使用電力KPI儀表板")
st.markdown("""
    本儀表板展示了各國地方政府在2017年的能源消耗數據，並提供了以下分析：
    - 各國地方政府的總用電量
    - 能源類型的消耗占比
    - C40 成員國與非成員國的能源使用比較
""")


# 使用 selectbox 選擇分析模式
all_countries = df['Country'].dropna().unique()

select_country = st.multiselect("請選擇國家進行分析（可複選）："
, sorted(all_countries), default=sorted(all_countries))

df = df[df['Country'].isin(select_country)]

import plotly.express as px

# 國家用電量視覺化
st.subheader("🌍 各國地方政府能源消耗（kWh）")
fig_bar = px.bar(
    df.groupby('Country')['Amount_kWh'].sum().reset_index().sort_values(by='Amount_kWh', ascending=False),
    x='Country', y='Amount_kWh',
    title='Total Local Government Energy Usage by Country (kWh)',
    labels={'Amount_kWh': 'Energy Consumption (kWh)'}
)
st.plotly_chart(fig_bar, use_container_width=True)

# 能源類型圓餅圖
st.subheader("🔌 能源消耗占比（依類型）")
type_summary = df.groupby('Type')['Amount_kWh'].sum().reset_index()
fig_pie = px.pie(
    type_summary,
    names='Type',
    values='Amount_kWh',
    title='Energy Consumption by Type (kWh)',
    hole=0.3
)
st.plotly_chart(fig_pie, use_container_width=True)

# C40 vs 非 C40 能源使用比較
st.subheader("🏙️ C40 成員國 vs 非成員國能源使用比較")
df['C40_flag'] = df['C40'].apply(lambda x: 1 if pd.notna(x) else 0)
c40_group = df.groupby('C40_flag')['Amount_kWh'].sum().reset_index()
c40_group['C40 類別'] = c40_group['C40_flag'].map({1: 'C40 成員國', 0: '非成員國'})
fig_c40 = px.bar(
    c40_group,
    x='C40 類別', y='Amount_kWh',
    title='C40 成員國 vs 非成員國 - 能源使用量比較',
    labels={'Amount_kWh': 'Energy Consumption (kWh)', 'C40 類別': '國家分類'},
    color='C40 類別'
)

st.plotly_chart(fig_c40, use_container_width=True)


