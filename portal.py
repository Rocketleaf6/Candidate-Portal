import streamlit as st
from supabase import create_client
import time

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

st.title("Candidate Submission Portal")

name = st.text_input("Candidate Name")
dob = st.text_input("DOB (DD/MM/YYYY)")
role = st.text_input("Role")
role_desc = st.text_area("Role Description")

cv = st.file_uploader("Upload CV", type=["pdf","docx"])
personal_excel = st.file_uploader("Upload Personal Excel", type=["xlsx"])

if st.button("Submit Candidate"):

    cv_path = ""
    excel_path = ""

    if cv:
        cv_path = f"resumes/{int(time.time())}_{cv.name}"
        supabase.storage.from_("Candidates Files").upload(
            cv_path,
            cv.getvalue()
        )

    if personal_excel:
        excel_path = f"personal_excel/{int(time.time())}_{personal_excel.name}"
        supabase.storage.from_("Candidates Files").upload(
            excel_path,
            personal_excel.getvalue()
        )

    supabase.table("Candidates").insert({
        "name": name,
        "dob": dob,
        "role": role,
        "role_description": role_desc,
        "cv_url": cv_path,
        "personal_excel_url": excel_path
    }).execute()

    st.success("Candidate Uploaded Successfully")
