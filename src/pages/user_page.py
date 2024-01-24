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


res = requests.get(
    url="http://localhost:8000/current_user",
    cookies={"find_malwares": cookies.get("find_malwares")},
)
if res.status_code == 200:
    st.header(f"Hello, {res.json()['username']}")
    st.subheader(f"Your email: {res.json()['email']}")
    st.subheader(f"Your current balance: {res.json()['balance']}")
else:
    st.error("You are unauthorized")

st.divider()
st.subheader("Do you want to topup you balance?")
amount = st.text_input("Amount of credits")
if st.button("Topup balance"):
    res = requests.post(
        url="http://localhost:8000/history/balance_topup",
        params={"amount": int(amount)},
        cookies={"find_malwares": cookies.get("find_malwares")},
    )
    if res.status_code == 200:
        st.rerun()
    elif res.status_code == 401:
        st.error("You are unauthorized")
    else:
        st.error("Something went wrong! You have the same balance.")

st.divider()
if st.button("Logout"):
    res = requests.post(
        url="http://localhost:8000/auth/logout",
        cookies={"find_malwares": cookies.get("find_malwares")},
    )
    if res.status_code == 204:
        cookies.clear()
        st.switch_page("main_page.py")
    else:
        st.error("Your are still in the system")
