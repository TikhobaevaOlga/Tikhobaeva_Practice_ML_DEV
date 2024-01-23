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

st.header("Predictions history")

res = requests.get(
    url="http://localhost:8000/history/prediction_history",
    cookies={"find_malwares": cookies.get("find_malwares")},
)
if res.status_code == 200:
    st.dataframe(res.json())
else:
    st.error('You are unauthorized')

st.header("Transaction history")

res = requests.get(
    url="http://localhost:8000/history/transaction_history",
    cookies={"find_malwares": cookies.get("find_malwares")},
)
if res.status_code == 200:
    st.dataframe(res.json())
else:
    st.error('You are unauthorized')