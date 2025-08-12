from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pathlib import Path
from dotenv import load_dotenv
from src.blueprints.upload import upload_bp


dotenv_path = Path(__file__).parents[1] / '.env'
load_dotenv(dotenv_path=dotenv_path)


app = Flask(__name__)
CORS(app)  # Allow CORS for all domains (local development)

app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['OUTPUT_FOLDER'] = os.getenv('OUTPUT_FOLDER')
app.config['AZURE_DOC_ENDPOINT'] = os.getenv("AZURE_DOC_ENDPOINT")
app.config['AZURE_DOC_KEY'] = os.getenv("AZURE_DOC_KEY")

app.config['AZURE_OPENAI_API_KEY'] = os.getenv("AZURE_OPENAI_API_KEY") 
app.config['AZURE_OPENAI_ENDPOINT'] = os.getenv("AZURE_OPENAI_ENDPOINT") 
app.config['AZURE_OPENAI_API_VERSION'] = os.getenv("AZURE_OPENAI_API_VERSION") 
app.config['AZURE_OPENAI_DEPLOYMENT_NAME'] = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

app.config['AZURE_STORAGE_CONNECTION_STRING'] = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

app.config['POPPLER_PATH'] = os.getenv("POPPLER_PATH", r"C:\Users\SivaTejaswiAnnangi\Downloads\QC folder\Release-24.08.0-0\poppler-24.08.0\Library\bin")

for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
    if not os.path.exists(folder):
        os.makedirs(folder)


@app.route('/')
def home():
    return "Welcome!"

app.register_blueprint(upload_bp)

    