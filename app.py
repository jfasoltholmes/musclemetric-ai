from flask import Flask, jsonify, request, render_template, flash, url_for, redirect
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from werkzeug.utils import secure_filename

# Load OpenAI API key from environment variables
load_dotenv()
secret_key = os.getenv("OPENAI_API_KEY")
if not secret_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
client = OpenAI(api_key=secret_key)

# Generate a random secret key for Flask
# print(os.urandom(12).hex())

# Initialize Flask app 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'heif', 'webp', 'avif'}
UPLOAD_FOLDER = 'static/tmp'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)

# Function to check if the uploaded file is an allowed image type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    if not allowed_file(filename):
        return None
    return filename.rsplit('.', 1)[1].lower()

#Decorator to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')


#Decorator to handle OpenAI API calls, maybe seperate this into a main.py file later
@app.route('/scan', methods=['GET', 'POST'])
def scan():
    try:
        if request.method == 'POST':
            # Check to see if file is in the request
            if 'image-submission' not in request.files:
                flash("No file part in the request", "error")
                return render_template('index.html')
            imageSubmission = request.files['image-submission']
            # Check if the file is empty
            if imageSubmission.filename == '':
                flash("No file selected", "error")
                return render_template('index.html')
            # Check if the file exists and is of an allowed type
            if imageSubmission and allowed_file(imageSubmission.filename):
                # Get the image and store in static folder
                imageSubmission = request.files['image-submission']
                filename = secure_filename(imageSubmission.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imageSubmission.save(image_path)

                # Construct public URL for OpenAI API to access the image
                image_url = ""

                # Image successfully processed into memory, now call OpenAI API
                flash(f"File {imageSubmission.filename} successfully processed in memory!", "success")
                
                bfEstimate = client.chat.completions.create(
                    model="gpt-4o",
                    max_tokens=10,
                    temperature=0.2,
                    messages=[
                        {"role": "system", "content": "You are a fitness assistant that estimates body fat percentage from user-submitted images. Only provide a visual estimate based on the image. Do not make medical diagnoses. Keep responses concise, numerical, and non-judgmental. If the image is unclear or inappropriate, respond with 'Unable to analyze image.'"},
                        {"role": "user", "content": f"Estimate the body fat percentage range based on this image. Respond only with a range in percentage format (e.g., 10–12%). If the image is unclear or cannot be analyzed, respond with: 'Unable to analyze image.' Image: {data_url}"}
                    ]
                )

                bfEstimateStripped = bfEstimate.choices[0].message.content.strip()
                if bfEstimateStripped.lower() == "unable to analyze image.":
                    flash("Unable to analyze image. Please try a different image.", "error")
                    return render_template('index.html')
                else:
                    boc = client.chat.completions.create(
                        model="gpt-4o",
                        max_tokens=75,
                        temperature=0.4,
                        messages=[
                            {"role": "system", "content": "You are a fitness assistant that helps users decide whether to bulk or cut based on their physique. You will use the provided body fat estimate and visible muscularity from the image to give clear advice. Be factual, friendly, and concise. Avoid medical claims. If the image is unclear, say so."},
                            {"role": "user", "content": f"My estimated body fat is {bfEstimateStripped}. Using the estimated body fat and this image, should I bulk or cut? Respond in 25-50 words with a clear recommendation. Only suggest one option: bulk or cut. Image: {data_url}"}
                        ]
                    )


                return render_template('analysis.html', image_data=data_url, bfEstimate_response=bfEstimate.choices[0].message.content, boc_response=boc.choices[0].message.content)
            else:
                flash("Invalid file type. Please upload an image file.", "error")
                return render_template('index.html')
        else:
            # handle GET requests, probably not needed?
            return render_template('index.html')

    
    except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return render_template('index.html')
     

if __name__ == '__main__':
    # Remove the debug=True line to run in production mode
    # For production, you might want to use a WSGI server like Gunicorn or uWSGI
    app.run(debug=True)