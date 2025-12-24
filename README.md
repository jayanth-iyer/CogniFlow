# CogniFlow

> **AI-Powered Seller Onboarding Assistant** — Streamline e-commerce seller onboarding with intelligent automation.

## 🎯 What It Does

CogniFlow helps **Account Managers (AMs)** onboard sellers to e-commerce platforms faster by:

| Feature | Description |
|---------|-------------|
| 📄 **Document Management** | Upload, store, and track seller documents (business licenses, tax forms, identity proofs) |
| 🤖 **AI Assistant** | Chat with an AI agent to get guidance on onboarding steps, document requirements, and next actions |
| 📊 **Seller Tracking** | Monitor seller onboarding status from submission to approval |
| ⚡ **Workflow Automation** | Automate repetitive tasks like document verification reminders and status updates |

## 🚀 Key Workflows

### 1. Seller Registration
```
AM creates seller → Seller status: "pending"
```

### 2. Document Collection
```
Upload documents → Link to seller → Status: "documents_submitted"
```

### 3. Review & Approval
```
AI assists review → AM approves/rejects → Status: "approved" or "rejected"
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, Vite, TypeScript, Tailwind CSS, Shadcn UI, Framer Motion |
| Backend | Python, FastAPI, SQLModel, SQLite |
| AI/ML | LangGraph, Ollama (Llama 3.2), LangFuse |

---

## 📦 Quick Start

### Prerequisites
- **Node.js** (v18+)
- **Python** (3.12+)
- **uv** — [Install here](https://github.com/astral-sh/uv)
- **Ollama** — [Install here](https://ollama.com/) + run `ollama pull llama3.2`

### 1. Start Backend
```bash
cd backend
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn main:app --reload
```
→ API available at **http://localhost:8000**  
→ Swagger docs at **http://localhost:8000/docs**

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```
→ App available at **http://localhost:5173**

---

## 🔌 API Reference

### Sellers
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/sellers` | Create a new seller |
| `GET` | `/api/v1/sellers` | List all sellers (filter by status) |
| `GET` | `/api/v1/sellers/{id}` | Get seller details |
| `PATCH` | `/api/v1/sellers/{id}?status=` | Update seller status |

### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/documents/upload` | Upload a document |
| `GET` | `/api/v1/documents` | List all documents (filter by seller) |
| `GET` | `/api/v1/documents/{id}` | Get document details |

### AI Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/chat` | Chat with the onboarding AI assistant |

---

## 🧪 Running Tests

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

**Current coverage**: 24 tests across models, sellers, and documents.

---

## 📁 Project Structure

```
CogniFlow/
├── backend/
│   ├── agents/          # LangGraph AI agents
│   ├── models/          # Database schemas (Seller, Document)
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   ├── tests/           # Unit tests
│   ├── main.py          # FastAPI app entry
│   └── database.py      # SQLite configuration
├── frontend/
│   ├── src/components/  # React components
│   └── src/App.tsx      # Main application
└── docs/                # Phase walkthroughs
```

---

## 📚 Documentation

- [Phase 0: Initial Setup](docs/phase_0_walkthrough.md)
- [Phase 1: Hello World](docs/phase_1_walkthrough.md)
- [Phase 2: Database & Documents](docs/phase_2_walkthrough.md)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
