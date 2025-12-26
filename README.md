# 🛡️ Global Anonymizer Tool

An advanced, privacy-focused web application that automatically detects and redacts sensitive information (PII) from texts and documents using NLP (Natural Language Processing).

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)

## 🚀 Features

- **Multi-Format Support:** Process raw text, **PDF**, **DOCX**, and **TXT** files.
- **AI-Powered Detection:** Uses `Microsoft Presidio` and `Spacy (en_core_web_lg)` for high-accuracy entity recognition.
- **Smart Redaction:** Automatically masks:
  - 👤 Names (PERSON)
  - 📞 Phone Numbers
  - 📧 Email Addresses
  - 📍 Locations
  - 📅 Dates
  - 🆔 ID Numbers / NRP
- **Visual Feedback:** Color-coded highlighting of redacted entities.
- **Export Options:** Download the sanitized result as **.TXT**, **.PDF**, or **.DOC**.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **AI/NLP:** Spacy, Presidio Analyzer & Anonymizer
- **File Handling:** PyPDF, Python-Docx
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, jsPDF

## ⚙️ Installation & Setup

Clone the repository and install the dependencies to run the project locally.

### 1. Clone the Repo
```bash
git clone [https://github.com/kullaniciadin/anonim-backend.git](https://github.com/kullaniciadin/anonim-backend.git)
cd anonim-backend
