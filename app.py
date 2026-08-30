import streamlit as st
from database import init_db, insert_record, get_all_records
from redundancy_checker import validate_and_classify

init_db()

st.title("Data Redundancy Removal System")
st.header("Add New Record")

name = st.text_input("Name")
email = st.text_input("Email")

if st.button("Submit"):
    if not name or not email:
        st.error("Name and email required")
    else:
        result = validate_and_classify(name, email)
        if result['status'] == 'accepted':
            insert_record(name, email, result['hash'])
            st.success("Record added successfully")
        elif result['status'] == 'rejected':
            st.warning("Exact duplicate rejected")
        else:
            st.info(result.get('message', 'Flagged for review'))

st.header("All Records")
records = get_all_records()
st.table(records)