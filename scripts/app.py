from glob import glob

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager,  rc
import streamlit as st
from PIL import Image

rc('font', family='AppleGothic')

plt.rcParams['axes.unicode_minus'] = False


def get_store_dfs():

    df = pd.read_excel('맛있는메뉴.xlsx')
    df = df.sort_values(by='review_dt')
    df['review_token'] = df['review_text'].str.split()
    df['review_token'] = df['review_token'].str.len()
    store_groups = df.groupby('store_name')
    store_dfs = {store: store_groups.get_group(store) for store in store_groups.groups}

    store_dfs_cumulative = {}

    for store, group in store_dfs.items():
        group = group.sort_values(by='review_dt')

        group['cumulative_review_length'] = group['review_token'].cumsum()

        # 결과를 저장
        store_dfs_cumulative[store] = group
    return store_dfs_cumulative

df = pd.read_parquet("monthly_review_count.parquet")
df.review_month = df.review_month.dt.to_timestamp()
store_dfs_cumulative = get_store_dfs()
target_stores = df.store_name.unique()


store_name = st.selectbox(
    '리뷰 내용이 궁금한 레스토랑을 선택해주세요',
    target_stores)


if store_name in store_dfs_cumulative.keys():
    group = store_dfs_cumulative[store_name]
    fig = plt.figure(figsize=(10,5))
    plt.plot(group['review_dt'], group['cumulative_review_length'], marker='o', color='b')
    plt.title(f' {store_name}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Review Length')
    plt.grid(True)
    plt.xticks(rotation=30)
    st.pyplot(fig)
else:
    st.text(f"NO SUCH STORE: {store_name}")




# streamlit run app.py --server.port 80



