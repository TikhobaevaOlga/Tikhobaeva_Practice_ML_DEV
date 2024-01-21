import json
import streamlit as st
import requests

st.title("Malware Classification App")
st.header("Registration")

st.write("Please fill in all fields to create a new account")

email = st.text_input("Email")
username = st.text_input("Username")
password = st.text_input("Password")

inputs = {
    "email": email,
    "username": username,
    "password": password,
}

if st.button('Submit'):
    res = requests.post(url = "http://localhost:8000/auth/register", data=json.dumps(inputs))
    st.subheader(f"Response from API * = {res.status_code}")