import streamlit as st
from supabase import create_client
import time
import re
import pandas as pd
from scoring_engine import (
    calculate_numbers_from_dob,
    evaluate_candidate_for_role,
)


SUPABASE_URL = st.secrets["SUPABASE_URL"].strip()
SUPABASE_KEY = st.secrets["SUPABASE_KEY"].strip()

if not SUPABASE_URL.startswith("https://"):
    st.error(f"Invalid Supabase URL: {SUPABASE_URL}")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


st.title("Candidate Submission Portal")

tab1, tab2 = st.tabs(["Candidate Upload", "Role Master"])

with tab1:
    # Load roles dynamically from Role Master table.
    roles_response = supabase.table("roles").select("*").execute()
    roles_data = roles_response.data or []
    role_names = ["Select Role"] + [r["role_name"] for r in roles_data if r.get("role_name")]
    selected_role = st.selectbox(
        "Role",
        role_names,
        index=0
    )

    selected_role_description = ""
    if selected_role != "Select Role":
        selected_role_description = next(
            r.get("role_description", "")
            for r in roles_data
            if r.get("role_name") == selected_role
        )

    st.text_area(
        "Role Description",
        value=selected_role_description,
        disabled=True
    )

    # ============================================
    # FORM INPUT
    # ============================================

    name = st.text_input("Candidate Name")
    dob = st.text_input("DOB (DD/MM/YYYY)")

    cv = st.file_uploader("Upload CV", type=["pdf", "docx"], key="cv_upload")
    personal_excel = st.file_uploader(
        "Upload Personal Excel",
        type=["xlsx"],
        key="excel_upload",
    )

    # ============================================
    # SUBMIT BUTTON
    # ============================================

    if st.button("Submit Candidate", key="submit_candidate"):
        if selected_role == "Select Role":
            st.error("Please select role")
            st.stop()

        cv_path = ""
        excel_path = ""

        # Upload CV
        if cv:
            safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', cv.name)
            cv_path = f"resumes/{int(time.time())}_{safe_name}"
            supabase.storage.from_("candidates-files").upload(
                cv_path,
                cv.getvalue()
            )

        # Upload Excel
        if personal_excel:
            safe_excel_name = re.sub(r'[^a-zA-Z0-9._-]', '_', personal_excel.name)
            excel_path = f"excel/{int(time.time())}_{safe_excel_name}"
            supabase.storage.from_("candidates-files").upload(
                excel_path,
                personal_excel.getvalue()
            )

        # Run numerology scoring before insert.
        birth, destiny, month = calculate_numbers_from_dob(dob)
        result = evaluate_candidate_for_role(
            birth,
            destiny,
            month,
            selected_role,
            selected_role_description
        )

        score = None
        verdict = None
        if isinstance(result, dict):
            score = result.get("Final Score")
            verdict = (result.get("Suitability Verdict") or {}).get("Risk Status")
        if score is None and hasattr(result, "overall_score_100"):
            score = float(result.overall_score_100)
        if verdict is None and hasattr(result, "risk_status"):
            verdict = str(result.risk_status)

        score = float(score if score is not None else 0.0)
        verdict = str(verdict if verdict is not None else "FAIL").upper()

        # Save to database
        supabase.table("Candidates").insert({
            "name": name,
            "dob": dob,
            "role": selected_role,
            "role_description": selected_role_description,
            "cv_url": cv_path,
            "personal_excel_url": excel_path if personal_excel else None,
            "score": score,
            "verdict": verdict,
            "stage": "Review Pending",
        }).execute()

        st.success("Candidate Uploaded Successfully")

    st.subheader("Uploaded Candidates")

    response = supabase.table("Candidates").select("*").execute()

    if response.data:

        df = pd.DataFrame(response.data)

        # Keep only required columns
        df = df[[
            "name",
            "role",
            "verdict",
            "stage"
        ]]

        # Rename headers nicely
        df.columns = [
            "Name",
            "Role",
            "Verdict",
            "Stage"
        ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No candidates uploaded yet.")

with tab2:
    st.subheader("Create New Role")

    role_name_input = st.text_input("Role Name", key="role_name_input")
    role_description_input = st.text_area("Role Description", key="role_description_input")

    if st.button("Save Role", key="save_role"):
        if not role_name_input or not role_description_input:
            st.error("Enter role name and description")
        else:
            supabase.table("roles").insert({
                "role_name": role_name_input,
                "role_description": role_description_input
            }).execute()
            st.success("Role saved successfully")

    st.subheader("Existing Roles")
    roles_response = supabase.table("roles").select("*").execute()

    for role in roles_response.data or []:
        if st.button(
            role["role_name"],
            key=f"edit_role_{role['id']}"
        ):
            st.session_state["edit_role_id"] = role["id"]

    if "edit_role_id" in st.session_state:
        role_id = st.session_state["edit_role_id"]
        role_data = next(
            r for r in (roles_response.data or [])
            if r["id"] == role_id
        )

        @st.dialog("Edit Role")
        def edit_role_dialog():
            new_name = st.text_input(
                "Role Name",
                value=role_data["role_name"]
            )

            new_desc = st.text_area(
                "Role Description",
                value=role_data["role_description"]
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Save"):
                    supabase.table("roles").update({
                        "role_name": new_name,
                        "role_description": new_desc
                    }).eq("id", role_id).execute()

                    st.success("Role updated")
                    del st.session_state["edit_role_id"]
                    st.rerun()

            with col2:
                if st.button("Cancel"):
                    del st.session_state["edit_role_id"]
                    st.rerun()

        edit_role_dialog()
