from flask import Flask, jsonify, request, render_template, flash, url_for, redirect
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from werkzeug.utils import secure_filename

# Load OpenAI API key from environment variables
load_dotenv()
secret_key = os.getenv("OPENAI_API_KEY")
if not secret_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

client = OpenAI(api_key=secret_key)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)

# Check if the uploaded file is an allowed extension type.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mime_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == "png":
        return "image/png"
    if ext in {"jpg", "jpeg"}:
        return "image/jpeg"
    return None


#Decorator to render the main HTML page.
@app.route('/')
def index():
    return render_template('index.html')


#Decorator to handle OpenAI API calls, maybe seperate this into a main.py file later
@app.route('/scan', methods=['POST'])
def scan():
    try:
        if 'image-submission' not in request.files:
            flash("No file part in the request", "error")
            return render_template('index.html')
        
        image_file = request.files['image-submission']

        if image_file.filename == '':
            flash("No file selected", "error")
            return render_template('index.html')
        
        if not allowed_file(image_file.filename):
            flash("Invalid file type. Please upload a PNG, JPG, or JPEG image.", "error")
            return render_template('index.html')
        
        mime_type = get_mime_type(image_file.filename)
        if not mime_type:
            flash("Unsupported image type.", "error")
            return render_template('index.html')
        
        image_bytes = image_file.read()
        if not image_bytes:
            flash("Uploaded file is empty.", "error")
            return render_template('index.html')
        
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:{mime_type};base64,{base64_image}"

        
        # Get the image and store in static folder
        '''
        imageSubmission = request.files['image-submission']
        filename = secure_filename(imageSubmission.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imageSubmission.save(image_path)
        '''

        # Construct public URL for OpenAI API to access the image
        image_url = ""

        # Image successfully processed into memory, now call OpenAI API
        flash(f"File successfully processed in memory!", "success")
        
        bf_estimate = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "You are a fitness assistant that estimates body fat percentage"
                                "from user-submitted images. Only provide a visual estimate based"
                                "on the image. Do not make medical diagnoses. Keep responses concise, "
                                "numerical, and non-judgemental. If the image is unclear or inappropriate, "
                                "respond with 'Unable to analyze image.'"
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Estimate the body fat percentage range based on this image. "
                                "Respond only with a range in percentage format (e.g., 10-12%). "
                                "If the image is unclear or cannot be analyzed, respond with: "
                                "'Unable to analyze image.'"
                            ),
                        },
                        {
                            "type": "input_image",
                            "image_url": data_url,
                        },
                    ],
                },
            ],
            max_output_tokens=20,
        )

        bf_estimate_text = bf_estimate.output_text.strip()

        if bf_estimate_text.lower() == "unable to analyze image.":
            flash("Unable to analyze image. Please try a different image.", "error")
            return render_template('index.html')

        return render_template('analysis.html', image_data=data_url, bfEstimate_response=bf_estimate_text)

    except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return render_template('index.html')
     

if __name__ == '__main__':
    # Remove the debug=True line to run in production mode
    # For production, you might want to use a WSGI server like Gunicorn or uWSGI
    app.run(debug=True)