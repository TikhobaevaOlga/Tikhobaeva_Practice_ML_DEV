import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager


cookies = EncryptedCookieManager(
    password="My secret password",
)
if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.stop()

if "data" not in st.session_state:
    st.session_state.data = {}

st.title("Malware Classification App")
st.header("Do you what to khow if your app is malware?")

st.subheader("You can choose one of the available models")

res = requests.get(
    url="http://localhost:8000/history/available_models",
    cookies={"find_malwares": cookies.get("find_malwares")},
)
if res.status_code == 200:
    st.dataframe(res.json())
else:
    st.error("You are unauthorized")

chosen_model = st.text_input("Write the name of the model here")
input_data = st.file_uploader("Choose a CSV file with input data", type="csv")


if st.button("Predict"):
    if chosen_model == "":
        st.write("Name of the model cannot be missing")
    else:
        res_task = requests.post(
            url="http://localhost:8000/prediction/",
            params={"model_name": chosen_model},
            files={"file": input_data.getvalue()},
            cookies={"find_malwares": cookies.get("find_malwares")},
        )
        if res_task.status_code == 201:
            st.session_state.data["saved_value"] = res_task.json()["task_id"]
            st.success(res_task.json()["task_id"])
        elif res_task.status_code == 401:
            st.error("You are unauthorized")
        else:
            st.error("Something went wrong!")

st.subheader("You can see the result on history page or after the click on the button")
if st.button("Knew result"):
    if "saved_value" not in st.session_state.data:
        st.error("You haven't asked for prediction yet ")
    else:
        res_result = requests.get(
            url=f"http://localhost:8000/prediction/{st.session_state.data['saved_value']}",
            cookies={"find_malwares": cookies.get("find_malwares")},
        )
        res_result = res_result.json()
        if res_result.get("result", None):
            st.success(res_result["result"])
        else:
            st.warning(res_result["status"])
