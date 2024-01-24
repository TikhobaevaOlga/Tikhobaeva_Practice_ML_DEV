import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager


cookies = EncryptedCookieManager(
    password="My secret password",
)
if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.stop()


st.title("Malware Classification App")
st.header("Login")

st.write(
    "Please login to have an access to a all functions.",
    "If you don't have an account, go to register page and create one."
)

email = st.text_input("Email")
password = st.text_input("Password")

inputs = {
    "username": email,
    "password": password,
}

if st.button("Submit"):
    res = requests.post(url="http://localhost:8000/auth/login", data=inputs)
    if res.status_code == 204:
        st.success("Login successful")
        cookies["find_malwares"] = res.cookies.get("find_malwares")
        cookies.save()
    else:
        st.error("Login failed")
