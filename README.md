# Upfolio

Resume analysis application that parses an uploaded resume, compares it against an
optional job description, and returns a deterministic ATS-compatibility score with
section-level breakdown, matched/missing skills, and actionable suggestions.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React 18, Vite 5, Tailwind CSS 3, React Router 6, Recharts, Framer Motion |
| Backend | Flask 3, Pydantic 2, scikit-learn, NLTK |
| Document parsing | PyMuPDF, pdfplumber (PDF), python-docx (DOCX) |
| Testing | pytest |

There is no database. Uploaded files are written to `backend/uploads/` and analysis is
computed in memory per request.

## Prerequisites

- Python 3.12
- Node.js 18 or later

## Project Structure

```
backend/
  app.py               Flask app factory and dev server (port 5000)
  config.py            Paths, limits, SECRET_KEY
  routes/analyze.py    POST /api/upload
  parsers/             PDF and DOCX text extraction
  extractors/          Section detection and structured resume building
  requirements/        Job description parser (Python package)
  scoring/ats_scorer.py  ATS scoring engine
  nlp/                 NLTK preprocessing and TF-IDF keyword discovery
  data/jd_corpus.py    Reference JD corpus used for TF-IDF
  models/              Pydantic schemas
  utils/               Logging, file handling, regex patterns and SKILLS_DB
  tests/               pytest suite
frontend/
  src/pages/           Home, Upload
  src/components/      UI, upload and results components
  src/services/api.js  Axios client
  src/data/            Static UI content and sample job descriptions
```

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
python app.py
```

The API serves on `http://localhost:5000` with Flask debug mode enabled.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server runs on `http://localhost:5173`. Vite proxies `/api/*` to
`http://localhost:5000`, so the client only ever issues relative requests.

Production build:

```bash
npm run build      # outputs to dist/
npm run preview    # serves the built bundle locally
```

## Configuration

No `.env` file is required. One environment variable is read:

| Variable | Default | Purpose |
| --- | --- | --- |
| `SECRET_KEY` | `upfolio-dev-secret-key` | Flask session signing key. Set this explicitly outside local development. |

Upload constraints are defined in `backend/config.py`: PDF and DOCX only, 10 MB maximum.

## API Reference

### `POST /api/upload`

`multipart/form-data`

| Field | Required | Description |
| --- | --- | --- |
| `resume` | Yes | Resume file, `.pdf` or `.docx`, max 10 MB |
| `job_description` | No | Raw job description text used for comparison |

Response `200`:

```json
{
  "success": true,
  "filename": "a1b2c3d4e5f6a7b8_resume.pdf",
  "pages": 1,
  "text": "raw extracted text",
  "parsedData": { "skills": [], "experience": [], "education": [] },
  "jdRequirements": {},
  "analysis": {
    "atsScore": 78,
    "sectionScores": {},
    "matchedSkills": [],
    "missingSkills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "summary": ""
  }
}
```

Errors return `400` with `{"success": false, "error": "..."}`.

## Scoring Model

The overall ATS score is a weighted blend of five section scores defined in
`backend/scoring/ats_scorer.py`:

| Section | Weight |
| --- | --- |
| Skill match | 0.35 |
| Keyword match | 0.25 |
| Experience | 0.15 |
| Formatting | 0.15 |
| Education | 0.10 |

Scoring is rule-based and deterministic, so any score can be traced back to the
signals that produced it. When no job description is supplied, scoring falls back to a
generic benchmark: a curated skill database (`utils/patterns.py`) and a list of
action verbs.

TF-IDF keyword discovery compares the job description against a reference corpus of
job descriptions in `backend/data/jd_corpus.py` using cosine similarity.

## Testing

```bash
cd backend
python -m pytest
```

Tests must run from the `backend/` directory: `backend/conftest.py` places that
directory on the import path so modules resolve as `scoring.ats_scorer` and so on.

The frontend has no test setup configured.

## Notes

- On first analysis the backend downloads NLTK corpora (`punkt`,
  `averaged_perceptron_tagger`, `wordnet`, `omw-1.4`, `stopwords`) into
  `backend/nltk_data/`. That first request requires network access.
- Uploaded filenames are prefixed with a random token to avoid collisions.
- `getAnalysisHistory()` and `deleteAnalysis()` in `frontend/src/services/api.js`
  still return mocked data; only resume upload is wired to the backend.
- No Docker, CI, or deployment configuration is included. The Flask development
  server is intended for local use only.