import time
import streamlit as st
import hashlib
import json
import os

# File to store user data (in a real application, use a secure database)
USER_DATA_FILE = "data/user_data.json"

def load_users():
    if os.path.exists(USER_DATA_FILE):
        if os.path.getsize(USER_DATA_FILE) == 0:
            return {}
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    else:
        with open(USER_DATA_FILE, "w") as f:
            json.dump({}, f)
        return {}

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_in():
    users = load_users()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        if username in users and users[username] == hash_password(password):
            st.session_state.user = username
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def sign_up():
    users = load_users()
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if username in users:
            st.error("Username already exists")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters long")
        else:
            users[username] = hash_password(password)
            save_users(users)
            st.session_state.user = username
            st.success("Account created successfully!")
            st.rerun()

def main():
    st.markdown("# Finance Tracker - Authentication")

    if "user" in st.session_state:
        st.markdown(f"## Welcome back, {st.session_state.user}!")
        time.sleep(3)
        st.switch_page("Home.py")
        if st.button("Log Out"):
            del st.session_state.user
            st.rerun()
    else:
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        with tab1:
            sign_in()
        with tab2:
            sign_up()

if __name__ == "__main__":
    main()