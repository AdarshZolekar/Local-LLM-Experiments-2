# Deepseek Streamlit Chat

Production-ready Streamlit apps for running **Deepseek reasoning models** either **locally with Ollama** or **via Groq's OpenAI-compatible API**. Designed for quick setup, clean UX, and reproducible development.

---

## Why this repo

- Local-first privacy with **Deepseek R1 1.5B** on **Ollama**
- Cloud performance with **Deepseek R1 Distill Llama 70B** on **Groq LPUs**
- Streaming chat UI with optional reasoning display
- Clear, minimal code organized for students and teams

---

## Apps

- `deepseek-r1-streamlit.py` — Local, offline via **Ollama**.
- `deepseek-groq-streamlit.py` — Cloud, requires **GROQ_API_KEY**.

---

## Quickstart

### A) Local Ollama (offline)

1. Install Python 3.10+ and [Ollama](https://ollama.ai/).
2. Pull the model:
   ```bash
   ollama pull deepseek-r1:1.5b
   ```
3. Install deps and run:
   ```bash
   pip install -r Requirements.txt
   streamlit run deepseek-r1-streamlit.py
   ```

### B) Groq API (cloud)

1. Get an API key from Groq Console and set it at runtime in the sidebar or export it:
   ```bash
   export GROQ_API_KEY=your_key_here
   ```
2. Install deps and run:
   ```bash
   pip install -r Requirements.txt
   streamlit run deepseek-groq-streamlit.py
   ```

---

## Project structure

```text
.
├─ deepseek-groq-streamlit.py    
├─ deepseek-r1-streamlit.py     
├─ Requirements.txt             
├─ .env.example                  
├─ .gitignore
├─ License
├─ Contributing.md
├─ Security.md
├─ Docs/
│  └─ Troubleshooting.md
└─ .Github/
   └─ Workflows/
      └─ ci.yml
```

---

## Configuration

- **Groq**: Provide `GROQ_API_KEY` in the sidebar (already supported in the UI). You can also set it in your shell.
- **Ollama**: Ensure the `ollama` daemon is running and the `deepseek-r1:1.5b` model is pulled.

---

## Development

- Format and lint:
  ```bash
  pip install -r Requirements-dev.txt
  ruff check .
  ruff format .
  ```
- Run CI locally:
  ```bash
  pytest -q 
  ```

---

## Notes

- Reasoning display uses `<think>...</think>` tags. The UI hides this by default and shows it in an expander.
- The Groq app uses the OpenAI-compatible endpoint (`openai_api_base=https://api.groq.com/openai/v1`).

---

## License

MIT. See [License](License).

---

## Security

Do not commit real API keys. Use `.env` or runtime injection. See [Security.md](Security.md).
