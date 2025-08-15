"""
Streamlit Contract Reader Agent

Features
- Upload a contract PDF
- Extract text + word coordinates using PyMuPDF (pymupdf)
- Send the plain text to an LLM to propose suggested changes (JSON schema)
- Display suggestions in an interactive table with: clause, issue, rationale, risk, rewrite
- For each suggestion, click **View origin in PDF** to open the exact page with the matched clause highlighted
- Export suggestions to CSV/JSON and save annotated snapshot images

Setup
1) pip install -r requirements.txt
   (see `requirements` variable below to copy into your requirements.txt)
2) Set your OpenAI key (or whichever LLM provider you choose):
   export OPENAI_API_KEY="sk-..."
3) Run: streamlit run app.py

Notes
- The LLM is optional for quick prototyping; you can click "Use demo suggestions" to test the UI without an API key.
- Matching from a suggestion back to the source is done with fuzzy matching at the sentence level and then refined with token span alignment over the page's word boxes.
"""



import io
import os
import json
import base64
import tempfile

from pydantic import BaseModel, Field

import streamlit as st

from dotenv import load_dotenv
load_dotenv()

# Import ABBYY functions from src.abbyy
from src.abbyy import (
    abbyy_upload_file,
    abbyy_extract_text,
    concat_extracted_texts
)

from src.s3 import (
    upload_file_to_s3,
    get_signed_url
)

from src.agent import (
    run_agent
)

from src.astra import (
    insert_snippet
)

class AgentSuggestedContractChange(BaseModel):
  original_snippet: str = Field(..., description="The original snippet of the contract that you want to query or change.")
  modified_snippet: str = Field(None, description="The modified snippet of the suggested update that you want to make to the snippet.")
  question_from_agent: str = Field(None, description="A question that you would like to ask the user about the original snippet")
  hidden: bool = Field(False, description="Whether this suggestion is hidden from the user")

suggestions = []

def submit_change(original_clause: str, modified_clause: str):
    # Here you could save to a database or process further

    if original_clause and modified_clause:
        result = insert_snippet(original_clause, modified_clause, False)
        print("Inserted snippet:", result)

    return True


def accept_change(index: int, modified_snippet: str):
    suggestion = st.session_state["suggestions"][index]

    insert_snippet(suggestion["original_snippet"], modified_snippet)

    suggestion["hidden"] = True  # or whatever state change you want

def ignore_once(index: int):
    suggestion = st.session_state["suggestions"][index]
    suggestion["hidden"] = True

def ignore_forever(index: int):

    suggestion = st.session_state["suggestions"][index]

    insert_snippet(
        suggestion["original_snippet"],
        None,
        True
    )

    suggestion["hidden"] = True

async def upload_document(file_path: str):

    # Upload the file to s3

    upload_file_to_s3(file_path, file_path.split("/")[-1])

    signed_url = get_signed_url(file_path.split("/")[-1])

    # Send doc to ABBYY

    abbyy_response = abbyy_upload_file(signed_url)

    # Process ABBYY response

    abbyy_text = abbyy_extract_text(abbyy_response)

    # Concat text

    agent_res = await run_agent(abbyy_text)

    suggestions = agent_res if agent_res else []

    # Generate IDs for suggestions
    for i, suggestion in enumerate(suggestions):
        suggestion["id"] = i

    st.session_state["suggestions"] = suggestions

    return suggestions
