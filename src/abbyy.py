import os
import io
from wsgiref import headers
import requests
import time

def abbyy_upload_file(url: str) -> str:
	"""
	Upload a document to ABBYY Cloud OCR SDK for processing.
	Requires ABBYY API credentials set in environment variables:
	ABBYY_API_KEY
	"""
	abbyy_api_key = os.getenv("ABBYY_API_KEY")
	api_url = "https://api.abbyy.com/document-ai/v1-preview/models/image-to-text"
	headers = {
		"Authorization": f"Bearer {abbyy_api_key}",
		"Content-Type": "application/json"
	}
	payload = {
		"inputSource": {
		"url": url
		}
	}
	response = requests.post(api_url, headers=headers, json=payload)
	res_json = response.json()
	print(res_json)
	if response.status_code == 201:
		return res_json[0]["id"]
	else:
		return None

def abbyy_extract_text(id: str) -> str:

	"""
	Extract text from a PDF document using ABBYY Cloud OCR SDK.
	Returns the plain text of the document.
	Requires ABBYY API credentials set in environment variables:
	ABBYY_API_KEY
	"""

	abbyy_api_key = os.getenv("ABBYY_API_KEY")
	api_url = f"https://api.abbyy.com/document-ai/v1-preview/models/image-to-text/{id}"
	headers = {
		"Authorization": f"Bearer {abbyy_api_key}",
		"Content-Type": "application/json"
	}
	
	res_json = None
	for _ in range(10):  # Retry up to 10 times
		print("Checking ABBYY extraction status...")
		response = requests.get(api_url, headers=headers)
		if response.status_code == 200:
			res_json = response.json()
			print('Checking res: ', res_json)
			print('Status: ', res_json['meta']['status'])
			print("Is Progressing: ", res_json['meta']['status'] == "Processing")
			if res_json['meta']['status'] != "Processing":
				break
			else:
				time.sleep(1)
		else:
			time.sleep(1)
			
	print(res_json)
	return concat_extracted_texts(res_json)

def concat_extracted_texts(extracted_texts_json):
	"""
	Concatenate the extracted texts from the ABBYY response.
	"""
	concatenated_text = ""
	for page in extracted_texts_json['text']['layout']['pages']:
		for block in page['texts']:
			if 'lines' in block:
				for line in block['lines']:
					concatenated_text += line['text'] + "\n"
	return concatenated_text
