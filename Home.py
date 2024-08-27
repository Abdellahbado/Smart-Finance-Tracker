import streamlit as st
import pandas as pd
from datetime import datetime


def check_authentication():
    return "user" in st.session_state and st.session_state.user is not None


def main():
    st.set_page_config(page_title="Finance Assistant", page_icon="💰", layout="wide")

    if not check_authentication():
        st.warning("Please sign in or sign up to access Finance Assistant.")
        if st.button("Go to Sign In / Sign Up"):
            st.switch_page("pages/Auth.py")
        return

    st.title("Finance Assistant")

    page = st.selectbox(
        "Go to", ["Home", "Income and Expenses", "Transactions", "Saving Goals"]
    )

    if page == "Income and Expenses":
        st.switch_page("pages/Income_and_Expenses.py")

    elif page == "Transactions":
        st.switch_page("pages/Transactions.py")

    elif page == "Saving Goals":
        st.switch_page("pages/Saving_Goals.py")


if __name__ == "__main__":
    main()
