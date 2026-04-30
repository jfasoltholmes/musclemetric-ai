from flask import Flask, request, render_template, flash, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
import base64

from utils.config import get_env_var
from utils.file_utils import allowed_file, get_mime_type

# Load OpenAI API key from environment variables before service import
load_dotenv()
#openai_api_key = get_env_var("OPENAI_API_KEY")
flask_secret_key = get_env_var("FLASK_SECRET_KEY")

from services.openai_analysis import analyze_physique
from schemas.analysis import AnalysisStatus

app = Flask(__name__)
app.secret_key = flask_secret_key


#Decorator to render the main HTML page.
@app.route('/')
def index():
    return render_template('index.html')


#Decorator to handle OpenAI API calls
@app.route('/scan', methods=['POST'])
def scan():
    try:
        if 'image-submission' not in request.files:
            flash("No file part in the request", "error")
            return redirect(url_for('index'))
        
        image_file = request.files['image-submission']

        if image_file.filename == '':
            flash("No file selected", "error")
            return redirect(url_for('index'))
        
        if not allowed_file(image_file.filename):
            flash("Invalid file type. Please upload a PNG, JPG, or JPEG image.", "error")
            return redirect(url_for('index'))
        
        mime_type = get_mime_type(image_file.filename)
        if not mime_type:
            flash("Unsupported image type.", "error")
            return redirect(url_for('index'))
        
        image_bytes = image_file.read()
        if not image_bytes:
            flash("Uploaded file is empty.", "error")
            return redirect(url_for('index'))
        
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:{mime_type};base64,{base64_image}"
        
        analysis = analyze_physique(data_url)

        if analysis.status == AnalysisStatus.UNABLE_TO_ASSESS:
            flash("Unable to analyze image. Please try a clearer image.", "error")
            return redirect(url_for('index'))

        return render_template('analysis.html', image_data=data_url, analysis=analysis)

    except Exception:
        flash(f"Something went wrong while analyzing the image. Please try again.", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Remove the debug=True line to run in production mode
    # For production, you might want to use a WSGI server like Gunicorn or uWSGI
    app.run(debug=True)