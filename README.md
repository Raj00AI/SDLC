# Catalyst.AI (prototype)

AI-assisted trial health co-pilot demo: portfolio overview, study detail KPIs, risk register, meeting pack generator, and actions/decisions with traceability.

## Quickstart (Windows PowerShell)
1. Create/activate venv and install deps (if not already):
   - `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
2. Generate sample data + load local store:
   - `.\.venv\Scripts\python.exe -m catalyst_ai.cli generate-data --seed 7`
3. Run API (optional, used by the UI):
   - `.\.venv\Scripts\python.exe -m uvicorn catalyst_ai.api.main:app --reload --port 8000`
4. Run Streamlit:
   - `.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py`

## Artifacts
Generated packs are written to `.artifacts/`.

## Tests
- `.\.venv\Scripts\python.exe -m pytest -q`
