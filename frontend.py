from operator import index
import streamlit as st


import io

import asyncio

from src.functions import (
    upload_document,
    submit_change,
    accept_change,
    ignore_forever
)

"""
Streamlit Contract Reader Agent Frontend

This file contains the Streamlit UI and interacts with backend functions from main.py.
"""

buf = io.BytesIO()

st.set_page_config(page_title="Contract Reader Agent Demo", layout="wide")

st.title("📄 Contract Reader Agent Demo")

screen = st.sidebar.radio("Choose a screen:", ["AI Suggestions", "Submit Your Change"])

if screen == "AI Suggestions":
    st.subheader("Upload Contract PDF")
    upl = st.file_uploader("Choose a PDF", type=["pdf"])

    if upl:
        st.success("PDF uploaded!")
        # Direct function call to process document
        if st.button("Process Document", key="process_doc_btn"):
            with st.spinner("Processing document..."):
                try:
                    # Save uploaded file to disk
                    file_path = f"uploaded_{upl.name}"
                    print(file_path)
                    agent_res = asyncio.run(upload_document(file_path))
                    print(agent_res)
                    # agent_res is a list, not a dict
                    st.session_state["ai_suggestions"] = agent_res if agent_res else []
                    st.success("Document processed!")
                except Exception as e:
                    st.error(f"Processing error: {e}")

        st.subheader("AI Suggested Changes")
        # State for edits and ignored suggestions for AI suggestions
        if "edited_ai_suggestions" not in st.session_state:
            st.session_state["edited_ai_suggestions"] = {}
        if "ignored_ai_suggestions" not in st.session_state:
            st.session_state["ignored_ai_suggestions"] = set()
        if "ignored_ai_once" not in st.session_state:
            st.session_state["ignored_ai_once"] = set()
        if "accepted_ai_suggestions" not in st.session_state:
            st.session_state["accepted_ai_suggestions"] = set()

        ai_suggestions = st.session_state.get("ai_suggestions", [])
        for s in ai_suggestions:
            suggestion_id = s.get("id")
            if s.get("hidden"):
                continue
            with st.container():
                st.markdown(f"### Suggestion {suggestion_id + 1}")
                st.markdown(f"**Original Snippet:**")
                st.text_area(
                    f"Original Snippet",
                    value=s.get("original", s.get("original_snippet", "")),
                    height=120,
                    disabled=True,
                    key=f"original_snippet_{suggestion_id}"
                )
                st.markdown(f"**Updated Version:**")
                edited_text = st.session_state["edited_ai_suggestions"].get(
                    suggestion_id,
                    s.get("suggested", s.get("modified_snippet", ""))
                )
                st.session_state["edited_ai_suggestions"][suggestion_id] = st.text_area(
                    f"Updated Version",
                    value=edited_text,
                    height=120,
                    key=f"updated_version_{suggestion_id}"
                )
                st.markdown(f"**Question from Agent:**")
                st.write(s.get("question", s.get("reason", s.get("question_from_agent", ""))))
                cols = st.columns([1, 1, 1])
                with cols[0]:
                    if st.button("✅ Accept Change", key=f"accept_ai_{suggestion_id}"):
                        accept_change(
                            suggestion_id,
                            st.session_state["edited_ai_suggestions"][suggestion_id]
                        )
                        st.rerun()
                with cols[1]:
                    if st.button("🚫 Ignore this time", key=f"ignore_ai_once_{s.get('id')}"):
                        st.session_state["ignored_ai_once"].add(s.get("id"))
                        st.info("Suggestion ignored for this session.")
                with cols[2]:
                    if st.button("🛑 Ignore forever", key=f"ignore_ai_forever_{s.get('id')}"):
                        st.session_state["ignored_ai_suggestions"].add(s.get("id"))
                        ignore_forever(s.get("id"))
                        st.info("Suggestion will be ignored forever.")
    else:
        st.info("Upload a PDF to get started.")

elif screen == "Submit Your Change":
    st.subheader("Submit a Change from Another Document")
    original_clause = st.text_area("Original Clause", "", height=100)
    modified_clause = st.text_area("Modified Clause", "", height=100)
    if st.button("Submit Change"):
        if original_clause.strip() and modified_clause.strip():
            with st.spinner("Submitting your change..."):
                try:
                    # Direct function call (could be extended to save to DB)
                    result = submit_change(original_clause, modified_clause)
                    st.success("Your change has been submitted!")
                    st.write(f"**Original Clause:**\n{original_clause}")
                    st.write(f"**Modified Clause:**\n{modified_clause}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please fill in both fields before submitting.")
