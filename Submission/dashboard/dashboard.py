import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

def pertanyaan1(df):
    df['order_approved_at'] = pd.to_datetime(df['order_approved_at'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    df['approval_time'] = df['order_approved_at'] - df['order_purchase_timestamp']
    df['delivery_time'] = df['order_delivered_customer_date'] - df['order_purchase_timestamp']

    df['approval_time_days'] = df['approval_time'].dt.days
    df['delivery_time_days'] = df['delivery_time'].dt.days

    avg_approval_time = df['approval_time_days'].mean()
    avg_delivery_time = df['delivery_time_days'].mean()

    data = {
        'avg_approval': avg_approval_time,
        'avg_delivery': avg_delivery_time
    }
    
    return data
    

sns.set(style='dark')

# Load cleaned data
all_df = pd.read_csv("main_data.csv")

category_options = ["All Categories"] + list(all_df["product_category_name_english"].unique())
selected_category = st.sidebar.selectbox("Select a Product Category", category_options)

if selected_category == "All Categories":
    filtered_df = all_df
else:
    filtered_df = all_df[all_df["product_category_name_english"] == selected_category]

st.subheader('Pertanyaan 1: Rata-rata waktu orderan')
col1, col2 = st.columns(2)
pertanyaan1_answer = pertanyaan1(filtered_df)
with col1:
    st.metric("Di-approve", value=f"{pertanyaan1_answer['avg_approval']:.2f} hari")

with col2:
    st.metric("Dikirimkan", value=f"{pertanyaan1_answer['avg_delivery']:.2f} hari")


st.subheader('Pertanyaan 2: Score/review tiap kategori tiap score nya')

grouped_df = filtered_df.groupby(by=["product_category_name_english", "review_score"]).agg({
    "review_score": "count",
}).rename(columns={"review_score": "count"}).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=grouped_df, x="review_score", y="count", hue="product_category_name_english", ax=ax)
ax.set_xlabel("Review Score")
ax.set_ylabel("Count")
ax.set_title("Review Score Distribution by Product Category")
st.pyplot(fig)
