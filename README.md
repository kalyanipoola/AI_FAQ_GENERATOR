# Fieldnotes: Local RAG Workshop

A beginner-friendly, local-first RAG app for exploring document retrieval and grounded answers. Upload Markdown, plain text, or text-based PDF documents, inspect the passages retrieved for each question, and optionally generate an answer with a local Ollama model.

## What happens when you ask a question

1. Documents are read as text and split into overlapping, word-based chunks.
2. BM25 ranks chunks against the question. The index stays in memory and is rebuilt when a document is added or removed.
3. The best passages are sent to Ollama's local chat API with instructions to answer from evidence and cite source numbers.
4. If Ollama is unavailable, the app still returns the retrieved passages. It does not pretend a model-generated answer exists.

The included `knowledge/workshop-guide.md` is indexed at startup. Uploaded documents are stored in `data/documents/`, which is excluded from Git. This app has no account system or authentication and is intended for local workshop use; do not expose it to an untrusted network.

## Run locally

Requirements: Python 3.10 or newer. Ollama is optional.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The document search works immediately. To enable generated answers, install [Ollama](https://ollama.com), then in another terminal run:

```powershell
ollama pull qwen2.5:3b
ollama serve
```

The model is several gigabytes; skip this step on machines with limited time or disk space. Set `OLLAMA_MODEL` to another model name if needed. See `.env.example` for configuration values (environment variables must be set in the shell; the app does not load `.env` automatically).

## Verify

```powershell
python -m pytest -q
```

## Workshop prompts

- Ask the starter question, then identify which source passage supports the answer.
- Rephrase a question with synonyms and compare BM25 retrieval results.
- Upload a handout and ask for a detail that appears in it.
- Change the chunk size and overlap in `app/rag.py`; compare the source excerpts.
- Stop Ollama and observe that retrieval remains available.
- Inspect how the prompt handles a question that the context cannot answer.

## Current boundaries

BM25 is lexical, not semantic; synonym-heavy questions can miss relevant passages. PDF extraction works for text PDFs, not scanned images that need OCR. The app does not persist embeddings, conversation history, or a vector database. The prompt is a grounding aid, not a security boundary; retrieved documents are treated as untrusted context.