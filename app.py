import streamlit as st
import requests

st.title("Adverse Drug Event Reporting System")

drug_name = st.text_input("Enter Drug Name")
if st.button("Fetch Data"):
    response = requests.get(f"http://localhost:8000/fetch_data/?drug_name={drug_name}")
    data = response.json()
    st.write(data)

if st.button("Summarize Events"):
    summary_response = requests.post("http://localhost:8000/summarize/", json=data)
    st.subheader("Summary of Adverse Events")
    st.write(summary_response.json()["summary"])