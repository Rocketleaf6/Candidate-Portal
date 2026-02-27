import streamlit as st
from supabase import create_client
from scoring_engine import (
    calculate_numbers_from_dob,
    evaluate_candidate_for_role,
)


# ============================================
# PASTE YOUR SUPABASE DETAILS HERE
# ============================================

SUPABASE_URL = "PASTE_URL"

SUPABASE_KEY = "PASTE_ANON_KEY"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


st.title("Candidate Submission Portal")

tab1, tab2 = st.tabs(["Candidate Upload", "Role Master"])

with tab1:
    # Load roles dynamically from Role Master table.
    roles_response = supabase.table("roles").select("*").execute()
    roles_data = roles_response.data or []
    role_options = [r.get("role_name", "") for r in roles_data if r.get("role_name")]

    # ============================================
    # FORM INPUT
    # ============================================

    name = st.text_input("Candidate Name")
    dob = st.text_input("DOB (DD/MM/YYYY)")

    if role_options:
        role = st.selectbox("Role", role_options)
        selected_role = next((r for r in roles_data if r.get("role_name") == role), {})
        default_desc = selected_role.get("role_description", "") or ""
    else:
        st.warning("No roles found. Add roles in Role Master tab.")
        role = st.text_input("Role")
        default_desc = ""

    role_desc = st.text_area("Role Description", value=default_desc)

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
        cv_path = ""
        excel_path = ""

        # Upload CV
        if cv:
            cv_path = f"resumes/{cv.name}"
            supabase.storage.from_("files").upload(
                cv_path,
                cv.getvalue()
            )

        # Upload Excel
        if personal_excel:
            excel_path = f"personal_excel/{personal_excel.name}"
            supabase.storage.from_("files").upload(
                excel_path,
                personal_excel.getvalue()
            )

        selected_role = role
        selected_role_description = role_desc

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

        if verdict == "PASS":
            st.success(f"PASS — Score: {score:.1f}")
        else:
            st.error(f"FAIL — Score: {score:.1f}")
        st.success("Candidate Uploaded Successfully")

    st.subheader("Uploaded Candidates")
    data = supabase.table("Candidates").select("*").order("created_at", desc=True).execute()
    rows = data.data or []
    if not rows:
        st.info("No uploaded candidates yet.")
    else:
        for cand in rows:
            c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 1, 2])
            c1.write(cand.get("name", ""))
            c2.write(cand.get("role", ""))
            c3.write(cand.get("score", ""))
            c4.write(cand.get("verdict", ""))
            c5.write(cand.get("stage", "Review Pending"))

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
    roles = supabase.table("roles").select("*").execute()
    for r in roles.data or []:
        st.write(f"• {r['role_name']}")
