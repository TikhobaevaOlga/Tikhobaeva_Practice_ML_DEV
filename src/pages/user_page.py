import streamlit as st
import requests

st.title("Malware Classification App")
st.header("Your account")

res = requests.get(url = "http://localhost:8000/current_user")
st.subheader(f"Response from API * = {res.text}")