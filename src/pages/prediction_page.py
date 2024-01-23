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
st.header("Do you what to khow if your app is malware?")

st.subheader("You can choose one of the available models")

res = requests.get(
    url="http://localhost:8000/history/available_models",
    cookies={"find_malwares": cookies.get("find_malwares")},
)
if res.status_code == 200:
    st.dataframe(res.json())
else:
    st.error('You are unauthorized')

chosen_model = st.text_input('Write the name of the model here')
input_data = st.file_uploader('Choose a CSV file with input data', type="csv")

if st.button("Predict"):
    res_task = requests.post(
        url="http://localhost:8000/prediction/",
        params={
            'model_name': chosen_model
        },
        files={"file": input_data.getvalue()},
        cookies={"find_malwares": cookies.get("find_malwares")}
    )
    if res_task.status_code == 201:
        task_id = res_task.json()['task_id']
    elif res_task.status_code == 401:
        st.error('You are unauthorized')
    else:
        st.error("Something went wrong!")

st.subheader("You can see the result on history page or after the click on the button")
if st.button("Knew result"):
    res_result = requests.get(
    url=f"http://localhost:8000/history/{task_id}",
    cookies={"find_malwares": cookies.get("find_malwares")},
)
    if res_result.json()['result']:
        st.write(res_result.json()['result'])
    else:
        st.write(res_result.json()['status'])