# MuscleMetrics.ai 💪📊
<p align="center">
  <img src="images/demo.gif" width="500"/>
</p>

<p align="center">
  A Flask-based web application for visual physique analysis using AI-generated structured insights.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue" />
  <img src="https://img.shields.io/badge/Flask-WebApp-lightgrey" />
  <img src="https://img.shields.io/badge/OpenAI-Structured%20Outputs-green" />
  <img src="https://img.shields.io/github/stars/jfasoltholmes/musclemetrics-ai?style=social" />
</p>

## ⚡ Quick Start

Run the app locally:

```bash
git clone https://github.com/jfasoltholmes/musclemetrics-ai
cd musclemetrics-ai
mise install
uv sync
python app.py
```

## Why MuscleMetrics.ai?
MuscleMetrics.ai explores how structured AI outputs can be used to generate consistent, user-facing analysis from unstructured image inputs.

Instead of free-form responses, the system enforces:
 - Predictable structure
 - Controlled tone
 - Strict visual grounding

The goal is to make AI-generated feedback more reliable, constrained, and usable.

## Overview
MuscleMetrics.ai is a Flask-based web application that analyzes a user-uploaded image and returns a structured physique assessment.

## Architecture

### Backend
 - Flask routing (app.py)
 - Service layer for AI interaction
 - Utility layer for file validation + config
### AI Layer
 - OpenAI Responses API
 - Structured output parsing into Pydantic models
 - Strict prompt constraints to prevent hallucination
### Frontend
 - Drag-and-drop image upload UI
 - Vanilla JS interaction handling
 - Server-rendered templates (Jinja2)

## Features

### Implemented
 - Drag-and-drop image upload
 - In-memory image processing (no file storage)
 - File validation (extension checks)
 - OpenAI structured output integration
 - Schema-based response parsing
 - Loading state + UX feedback
 - Flash message handling
### Analysis Output
 - Estimated body fat range
 - Goal recommendation (bulk / cut / maintain / recomp)
 - Rationale and actionable guidance
 - Physique assessment:
    - Strengths
    - Weak points (if visible)
    - Fat distribution
 - Improvement priorities
 - Image quality note
 - Image-specific limitations

## Design Principles

- Visual-only analysis (no inference beyond observable features)
- No hallucinated feedback (avoids forced or invented insights)
- Structured responses (enforced schema for consistency)
- Minimalism over verbosity (concise, realistic output)

## Deployment Notes

Designed to run behind a WSGI server (e.g., Gunicorn)

Required environment variables:
 - `OPENAI_API_KEY`
 - `FLASK_SECRET_KEY`

## Tech Stack

- Python
- Flask
- JavaScript
- HTML/CSS
- Pydantic
- OpenAI API (Responses API + Structured Outputs)

## Repository Structure
```bash
musclemetrics-ai/
├── app.py                     # Flask app entry point + routes
│
├── schemas/                  # Data models and structured output schemas
│   └── analysis.py           # Pydantic models + enums for AI response
│
├── services/                 # External integrations and business logic
│   └── openai_analysis.py    # OpenAI API call + structured parsing
│
├── utils/                    # Shared helper utilities
│   ├── config.py             # Environment variable handling
│   └── file_utils.py         # File validation + MIME helpers
│
├── templates/                # HTML templates (Jinja2)
│   ├── index.html            # Upload page
│   └── analysis.html         # Results page
│
├── static/                   # Frontend assets
│   ├── main.css
│   ├── main.js
│   ├── analysis.css
│   └── analysis.js
│
├── .env                      # Environment variables (not committed)
├── .gitignore
│
├── pyproject.toml            # Python dependencies
├── uv.lock                   # Locked dependencies
├── mise.toml                 # Toolchain/version management
├── .python-version           # Python version
│
├── README.md
└── .venv/                    # Local virtual environment (ignored)
```