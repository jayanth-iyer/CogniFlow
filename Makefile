.PHONY: install dev-backend dev-frontend test

install:
	cd backend && uv pip install -r requirements.txt
	cd frontend && npm install

dev-backend:
	cd backend && uv run uvicorn main:app --reload

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && uv run pytest
