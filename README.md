# Contract Reader Agent

An MVP AI-powered agent that analyzes contract documents, suggests changes, and learns from user feedback. This project demonstrates the agent's "learning" process—how it adapts based on user interactions. In a production setting, a full-featured document editor would be required for practical use.

## 🎯 Use Cases

Designed for legal teams, contract managers, and anyone working with contracts who wants to:

- **Automatically analyze contracts** and receive AI-powered suggestions
- **Review and accept/ignore changes** suggested by the agent
- **Submit your own changes** for the agent to learn from
- **Showcase agent learning**: See how the agent adapts based on feedback

## 🚀 Features

- **PDF Upload & OCR**: Upload contract PDFs for analysis (requires ABBYY API or alternative OCR)
- **AI Suggestions**: View, edit, accept, or ignore AI-suggested contract changes
- **User Change Submission**: Submit your own contract edits for agent learning
- **Streamlit UI**: Simple, interactive frontend for contract review and feedback
- **Agent "Learning" Showcase**: Demonstrates how feedback can improve suggestions

## 🔧 How It Works

1. **Upload Contract**: Users upload a PDF contract via the Streamlit interface
2. **OCR & Processing**: The backend uses ABBYY API (or alternative) for OCR, storing files in AWS S3 for public access
3. **AI Suggestions**: The agent analyzes the contract and suggests changes, which users can review, edit, accept, or ignore
4. **User Feedback**: Users can submit their own changes, helping the agent "learn" and improve future suggestions
5. **Data Storage**: Suggestions and feedback are stored in DataStax AstraDB

### APIs & Services Used

- **ABBYY API** (or alternative OCR): For extracting text from PDFs
- **AWS S3**: For storing uploaded files and providing public URLs for OCR processing
- **DataStax AstraDB**: For storing contract data, suggestions, and user feedback

## 📋 Prerequisites

- Python 3.8+
- ABBYY API credentials (or alternative OCR provider)
- AWS S3 bucket and credentials
- DataStax AstraDB account and credentials

## ⚙️ Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-proj-12345

ABBYY_API_KEY=abbyy_12345

S3_BUCKET_NAME=your-bucket-name
AWS_REGION=eu-west-2
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key

ASTRA_DB_API_ENDPOINT=your-astra-db-api-endpoint
ASTRA_DB_APPLICATION_TOKEN=your-astra-db-application-token
ASTRA_DB_NAMESPACE=your-astra-db-namespace
ASTRA_DB_COLLECTION=snippets
```

## 🔧 Installation

### Local Development

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd contract-reader-agent
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    ```bash
    cp .env.example .env
    # Edit .env with your API keys and credentials
    ```

4. Run the Streamlit application:
    ```bash
    streamlit run frontend.py
    ```

5. Open your browser to `http://localhost:8501`

### Project Structure

```
contract-reader-agent/
├── frontend.py            # Streamlit UI
├── src/
│   └── functions.py       # Backend logic for document processing and agent actions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── .env.example           # Environment template
```

## 📝 Usage

### Web Interface

1. **Start the application**:
    ```bash
    streamlit run frontend.py
    ```
2. **Upload a contract PDF**:
    - Supported format: PDF
    - The agent will process the document and suggest changes
3. **Review AI Suggestions**:
    - Edit, accept, or ignore suggested changes
    - Submit your own changes for agent learning
4. **Feedback Loop**:
    - The agent adapts based on accepted/ignored suggestions and user submissions

## ⚠️ Limitations

- **MVP Only**: This is a prototype to showcase agent learning. A production system would require a full document editor and more robust feedback mechanisms.
- **OCR Dependency**: Requires ABBYY API or similar for PDF text extraction.
- **Cloud Services Required**: Needs AWS S3 and AstraDB setup.

## 🐛 Troubleshooting

- Ensure all API keys and credentials are set in `.env`
- Check S3 bucket permissions for public file access
- Verify ABBYY API limits and access
- Review Streamlit logs for error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with various contract PDFs
5. Submit a pull request

## 👨‍💻 Credits

Created by **Tom Shaw** - [https://github.com/IAmTomShaw](https://github.com/IAmTomShaw)

This project demonstrates how an AI agent can learn from user feedback in contract review workflows. For real-world use, a document editor and more advanced feedback integration would be required.