# `Google-Gemma-Chatbot-API` -> EN.AI Chatbot

> *"Initializing EN.AI engine..."*
> `[OK] Database connected.`
> `[OK] Gemini API client configured.`
> `[OK] Operator console ready.`

Welcome to **EN.AI**, an interactive chatbot terminal interface powered by the Gemini API and built with Flask. Featuring a premium, responsive glassmorphic design and a customized AI assistant persona, this system provides a secure, fully styled chat workspace directly in your web browser.

---

### `/usr/bin/features`

* **Secure Authentication:** User signup and sign-in built on SQLite3 with SHA-256 hashed credentials and Flask sessions.
* **Cyberpunk Aesthetics:** A custom glassmorphic UI styled with CSS radial depth gradients, animated smoke elements, glowing text, and invisible custom scrollbars.
* **Powered by Gemini:** Integrated with Google's `gemini-2.5-flash` model, equipped with real-time Google Search tools.
* **Translated Codebase:** Full English codebase including variables, route responses, HTML pages, code comments, and model system instructions.
* **Auto-Reloading Debugger:** Runs locally on a configurable port with Flask's active debugger and auto-reloading capability.

---

### `/etc/config`

Here's an overview of the core files powering this repository:

| File | Badges & Tech | Description |
| :--- | :--- | :--- |
| **[app.py](file:///home/rsalas/Documentos/Google-Gemma-Chatbot-API/app.py)** | ![](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) ![](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) | Main server script managing authentication, DB queries, UI template rendering, and conversational routes. |
| **[training.py](file:///home/rsalas/Documentos/Google-Gemma-Chatbot-API/training.py)** | ![](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![](https://img.shields.io/badge/Gemini_API-8E75C2?style=flat-square&logo=google&logoColor=white) | System instructions, role-playing, and persona definition that guide the chatbot to act as EN.AI. |

---

### `/home/raul/setup/`

Ready to initialize the operator console? Run the following commands in your terminal:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Start the Flask server:**
   ```bash
   python app.py
   ```
   *Note: The application will run locally on **http://127.0.0.1:5002** (or any port configured in the entrypoint).*

---
