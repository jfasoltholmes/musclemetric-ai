# MuscleMetrics.ai

An early Flask prototype for a physique-analysis web app.

This project was originally started as an experimental image-upload workflow where a user can drag and drop a photo, submit it through a Flask backend, and receive a rough OpenAI-powered analysis on a results page.

## Current State

This repo is an unfinished prototype and is being revived/refactored.

At the moment, the project includes:

- Flask backend
- Drag-and-drop image upload UI
- Basic file validation
- OpenAI API integration
- Preliminary results page
- Static frontend assets with vanilla JavaScript and CSS

Some parts are still rough or incomplete, including:

- Analysis flow cleanup
- Better backend/service separation
- Safer image handling
- Improved output structure
- Deployment readiness

## Notes

- Secrets are stored in environment variables and are not committed.
- This repo reflects an earlier stage of the project before a fuller refactor.
- A future refactor will likely move uploaded image handling into memory instead of saving files locally.

## Tech Stack

- Python
- Flask
- JavaScript
- HTML/CSS
- OpenAI API
- UV
- Mise

## Local Setup

1. Create a `.env` file with the required secrets:
  - `OPENAI_API_KEY`
  - `FLASK_SECRET_KEY`

2. Create and activate your environment.

3. Install dependencies.

4. Run the Flask app locally.

## Immediate Refactor Goals

- Stop saving uploaded files into `static/`
- Move analysis logic into a separate service layer
- Improve validation and error handling
- Return structured analysis results
- Prepare the app for deployment