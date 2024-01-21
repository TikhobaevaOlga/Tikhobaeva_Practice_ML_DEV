import streamlit as st
import requests

st.title("Malware Classification App")
st.header("Login")

st.write("Please login to have an access to a all functions. If you don't have an account go to register page and create one.")

email = st.text_input("Email")
password = st.text_input("Password")

inputs = {
    "username": email,
    "password": password,
}

if st.button('Submit'):
    res = requests.post(url = "http://localhost:8000/auth/login", data=inputs)
    st.subheader(f"Response from API * = {res.status_code}")