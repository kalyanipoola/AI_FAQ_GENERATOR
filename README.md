# AI FAQ Generator

## Project Overview

The AI FAQ Generator is a simple web application that generates Frequently Asked Questions (FAQs) and their answers for any topic using Artificial Intelligence.

The user enters a topic, selects the number of FAQs, and the application generates questions and answers using the Groq AI API.

---

## Features

* Enter any topic
* Select the number of FAQs
* Generate AI-based questions
* Generate AI-based answers
* Simple Streamlit interface

---

## Technologies Used

* Python
* Streamlit
* Groq AI API
* python-dotenv

---

## Files

* `app.py` – Main application
* `requirements.txt` – Required Python packages
* `.env.example` – Sample API key file
* `README.md` – Project documentation

---

## How to Run

1. Install the required packages.

```bash
pip install -r requirements.txt
```

2. Create a `.env` file and add your Groq API key.

```text
GROQ_API_KEY=your_api_key_here
```

3. Run the application.

```bash
streamlit run app.py
```

---

## Example

**Topic:** Python

The application generates AI-based Frequently Asked Questions and answers related to Python.

