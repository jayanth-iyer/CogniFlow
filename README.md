# CogniFlow

AI Assistant that automates workflows for Account Managers (AMs) who onboard sellers to e-commerce platforms.

## 🚀 Overview
CogniFlow leverages AI to streamline the seller onboarding process, from document verification to product listing generation and proactive communication.

## 🛠 Tech Stack
- **Frontend:** React, Vite, Shadcn UI, Framer Motion, Tailwind CSS
- **Backend:** Python + FastAPI (Managed by `uv`)
- **Database:** SQLite (Local) / SQLModel
- **AI/ML:** LangGraph, Ollama (Llama 3.2:3b), LangFuse

## 📁 Project Structure
- `frontend/`: React + Vite frontend application.
- `backend/`: FastAPI backend application.
- `docs/`: Phase-wise documentation and walkthroughs.

## 🚦 Getting Started

### Prerequisites
- Node.js & npm
- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.com/) (with `llama3.2` model)

### Setup
1. **Ollama:** `ollama pull llama3.2`
2. **Backend:**
   ```bash
   cd backend
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   uvicorn main:app --reload
   ```
3. **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📄 Documentation
Check the `docs/` folder for phase-wise walkthroughs and detailed architecture.
