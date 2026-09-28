# OpenRouter AI Chatbot

An intermediate-level, developer-grade AI Chatbot web application powered by **FastAPI** and the **OpenRouter API**.

This project provides a clean, responsive single-page web interface backed by a secure Python proxy that dynamically discovers available models, queries model metadata (context window, pricing, modality), validates your OpenRouter credentials, and conducts multi-turn conversations.

---

## 🔒 Security Architecture

```text
┌───────────────────────┐
│  Browser Client (UI)  │  <-- HTML5 / CSS3 / Vanilla JS
└───────────┬───────────┘
            │  Plain HTTP JSON (/api/chat, /api/test-key, /api/models)
            │  (NO SECRETS EVER SENT OR STORED ON CLIENT)
            ▼
┌───────────────────────┐
│ FastAPI Backend Proxy │  <-- Reads OPENROUTER_API_KEY from .env
└───────────┬───────────┘
            │  Authenticated HTTPS Requests with Bearer Token
            │  (Authorization: Bearer $OPENROUTER_API_KEY)
            ▼
┌───────────────────────┐
│    OpenRouter API     │  <-- https://openrouter.ai/api/v1
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Selected AI Model    │  (e.g., LLaMA 3.1, Claude 3.5, GPT-4o, Mistral)
└───────────────────────┘
```

- **Zero Client-Side Secret Exposure**: The frontend browser JavaScript, HTML, and CSS never contain, request, or receive the API key.
- **Environment Isolation**: `OPENROUTER_API_KEY` is loaded on the server via `python-dotenv` from `.env`.
- **Git Protection**: `.gitignore` is pre-configured to strictly prevent `.env`, virtual environments, and caches from being committed.
- **Safe Error Reporting**: Server exceptions and upstream OpenRouter responses are sanitized before being forwarded to the client.

---

## 📁 Project Structure

```text
openrouter-chatbot/
│
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application, route handlers, static file server
│   ├── openrouter_client.py    # OpenRouter API client service & error normalization
│   └── requirements.txt        # Python backend dependencies
│
├── frontend/
│   ├── index.html              # Clean semantic HTML5 chat interface & sidebar
│   ├── style.css               # Modern developer dark theme & responsive layout
│   └── app.js                  # Vanilla JS state, API testing, model loading & chat
│
├── .env.example                # Template for environment configuration
├── .gitignore                  # Prevents committing secrets & caches
└── README.md                   # Comprehensive guide and testing checklist
```

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Python 3.9+ installed on your system.
- An OpenRouter API Key (sign up and generate a key at [openrouter.ai/keys](https://openrouter.ai/keys)).

### 1. Navigate to Project Directory
```powershell
cd C:\Users\sateesh\.gemini\antigravity\scratch\openrouter-chatbot
```

### 2. Create and Activate a Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

*(If running into PowerShell script execution policy restrictions, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)*

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Open `.env` in your editor and insert your actual OpenRouter key:
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Start the FastAPI Development Server
```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Open the Application
Open your web browser and navigate to:
```text
http://127.0.0.1:8000
```
FastAPI automatically serves the single-page application at the root route `/`.

---

## 📖 API Documentation & Swagger UI

FastAPI generates automatic interactive OpenAPI documentation:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

You can test every endpoint directly through Swagger without opening the frontend.

---

## 🔍 How the Core Features Work

### 1. API Key Testing (`GET /api/test-key`)
- Reads `OPENROUTER_API_KEY` from the environment.
- Verifies that the variable is set and not empty or the placeholder string.
- Makes a lightweight call to OpenRouter's `/api/v1/auth/key` endpoint.
- Returns status, non-sensitive usage metrics (e.g. usage to date, credit limits), and whether the account is on a free tier.
- Never prints, logs, or returns the raw secret key.

### 2. Dynamic Model Discovery (`GET /api/models`)
- Fetches all available models directly from OpenRouter's `/api/v1/models`.
- Formats each model with:
  - Model ID (e.g., `meta-llama/llama-3.1-8b-instruct:free`)
  - Human-readable name
  - Provider (e.g., `meta-llama`, `anthropic`, `openai`)
  - Context window size
  - Prompt & Completion token pricing
  - Architecture modalities (e.g., `text->text`)
- The frontend dynamically groups and renders these into a searchable dropdown.

### 3. Chat Completions (`POST /api/chat`)
- Accepts a payload with:
  ```json
  {
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "messages": [
      { "role": "user", "content": "Hello!" }
    ],
    "temperature": 0.7
  }
  ```
- The backend verifies inputs, attaches the server-side bearer token, and proxies the request to OpenRouter's `/api/v1/chat/completions`.
- Maintains multi-turn context by forwarding preceding messages.
- Returns the assistant's reply and token usage statistics.

---

## 🧪 Testing Checklist

Follow this 10-step checklist to test the entire application end-to-end:

- [ ] **TEST 1: Start the server**
  Run `uvicorn backend.main:app --reload` and check that the server launches without errors at `http://127.0.0.1:8000`.

- [ ] **TEST 2: Open the web application**
  Navigate to `http://127.0.0.1:8000` in your browser. Verify the dark-themed developer studio UI, sidebar, and welcome screen render properly.

- [ ] **TEST 3: Click "Test API Key"**
  Click the **Test API Key** button in the left sidebar. Notice the status badge change to "Testing..." with a pulsing indicator.

- [ ] **TEST 4: Verify key status reporting**
  - If your `.env` contains a valid key: The badge turns green ("Active") and displays your account usage.
  - If `.env` is missing or invalid: The badge turns red ("Invalid") and displays a clear explanation without breaking the app.

- [ ] **TEST 5: Load available models**
  Verify the model dropdown populates automatically with models from OpenRouter. Try typing in the filter box (e.g., `free` or `llama`) to ensure real-time model searching works.

- [ ] **TEST 6: Select a model**
  Select a model (e.g., `meta-llama/llama-3.1-8b-instruct:free`). Verify that the **Model Metadata Card** reveals the Provider, Context Window, and Pricing per 1M tokens.

- [ ] **TEST 7: Send a message**
  In the bottom input box, type:
  ```text
  Hello, introduce yourself.
  ```
  Press **Enter** (or click the send button).

- [ ] **TEST 8: Verify assistant response**
  Verify that the user message appears on the right, the typing indicator animates while waiting, and the assistant's reply appears on the left with a timestamp, model tag, and copy button.

- [ ] **TEST 9: Multi-turn conversation history**
  Send a follow-up message:
  ```text
  What was the first question I asked you?
  ```
  Verify that the assistant remembers the prior message in the conversation.

- [ ] **TEST 10: Graceful error handling**
  Test an error scenario (e.g., temporarily provide an invalid model or run out of credits). Verify that the application displays a readable banner and error message rather than crashing.

---

## 🛠️ Common Errors & Fixes

| HTTP Status / Error | Cause | Resolution |
| :--- | :--- | :--- |
| **OPENROUTER_API_KEY is not set** | The `.env` file does not exist or the variable is empty. | Create `.env` based on `.env.example` and set `OPENROUTER_API_KEY=your_key`. |
| **HTTP 401 Unauthorized** | The API key entered is expired, revoked, or misspelled. | Check [openrouter.ai/keys](https://openrouter.ai/keys) to create or verify your key. |
| **HTTP 402 Insufficient Credits** | Your OpenRouter account balance has been exhausted. | Add credits to your OpenRouter account or select any model with the `:free` suffix (e.g., `meta-llama/llama-3.1-8b-instruct:free`). |
| **HTTP 404 Model Not Found** | The selected model is temporarily decommissioned or offline. | Click "Refresh" and select an active model from the dropdown. |
| **HTTP 429 Rate Limit Exceeded** | Too many requests sent in a short window. | Wait a few seconds before retrying. |
| **Network Timeout / 504** | OpenRouter upstream model took too long to generate. | Select a smaller/faster model or reduce message length. |
