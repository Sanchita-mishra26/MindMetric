# MindMetric

MindMetric is an educational student wellbeing frontend backed by the project's FastAPI prediction endpoint. The UI displays the actual `predicted_mental_health_score` returned by the API; it does not infer a label or diagnosis from the score.

## Run locally

Install the Python packages once:

```powershell
python -m pip install fastapi uvicorn pandas joblib scikit-learn
```

Install the frontend packages once, then start both services together from the project folder:

```powershell
npm install
npm run dev:all
```

This launches FastAPI at `http://127.0.0.1:8000` and Vite at `http://localhost:5173`. Open the Vite URL in your browser. Press `Ctrl+C` to stop both services.

To use another API URL, copy `.env.example` to `.env`, set `VITE_API_BASE_URL` to the API origin, and restart Vite:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The FastAPI CORS middleware permits the Vite development origin. `main.py` imports the middleware used in its existing CORS configuration.
