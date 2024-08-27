from datetime import datetime
import streamlit as st
import pandas as pd

st.title("Transactions")

# Load existing data
try:
    df = pd.read_csv("transactions.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Transaction", "Amount", "Category"])

# Input form
with st.form("transactions_form"):
    date = st.date_input("Date", value=datetime.today())
    transaction = st.text_input("Transaction")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.text_input("Category")
    submitted = st.form_submit_button("Add")

if submitted:
    new_row = {"Date": date, "Transaction": transaction, "Amount": amount, "Category": category}
    df = df.append(new_row, ignore_index=True)
    df.to_csv("transactions.csv", index=False)
    st.success("Transaction added successfully!")

st.dataframe(df)
