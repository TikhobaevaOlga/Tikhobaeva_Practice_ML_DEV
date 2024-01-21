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
st.header("Your account")


res = requests.get(
    url="http://localhost:8000/current_user",
    cookies={"find_malwares": cookies.get("find_malwares")},
)
st.subheader(f"Response from API * = {res.text}")
