# MuscleMetrics.ai

A Flask-based web application for visual physique analysis using AI-generated structured insights.

Users can upload an image and receive a structured, AI-generated assessment including estimated body fat range, training recommendation (bulk/cut/etc.), and physique feedback.

## Current State

This project has been refactored into a modular architecture and now supports structured AI responses.

### Design Principles

- Analysis is based strictly on visible features in the image
- The system avoids overgenerated or forced feedback (e.g., no invented weak points)
- Output is structured but intentionally restrained to improve realism and trust

### Implemented

- Flask backend with clean routing
- Drag-and-drop image upload UI
- In-memory image processing (no file persistence)
- File validation (type + basic checks)
- OpenAI API integration using image + structured outputs
- Single-call analysis pipeline using OpenAI structured outputs (reduced latency and cost)
- Pydantic schema for structured response parsing
- Service layer for AI logic (services/)
- Utility layer for config + file handling (utils/)

### Analysis Output Includes

- Estimated body fat range
- Recommended goal (bulk, cut, maintain, recomp)
- Rationale and actionable guidance
- Physique assessment:
  - Strengths
  - Weak points (if visible)
  - Body fat distribution
- Improvement priorities
- Image quality note
- Image-specific limitations and interpretation notes

## Tech Stack

- Python
- Flask
- JavaScript
- HTML/CSS
- Pydantic
- OpenAI API (Responses API + Structured Outputs)

## Local Setup

1. Create a `.env` file with the required secrets:
  - `OPENAI_API_KEY`
  - `FLASK_SECRET_KEY`

2. Create and activate your environment.

3. Install dependencies.

4. Run the Flask app locally.

## Immediate Goals

- Improve frontend UX and results presentation
- Handle edge cases in model output more gracefully
- Optimize prompts and response consistency
- Prepare for production deployment

## Repository Structure
```bash
MuscleMetrics.ai/
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
│   ├── main.css/
│   ├── main.js/
│   ├── analysis.css/
│   └── analysis.js/
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