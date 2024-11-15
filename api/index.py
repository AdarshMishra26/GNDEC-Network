from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, current_user
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# App configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGODB_URI')
}

# Initialize extensions
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configure mail
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS') == 'True',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
)
mail = Mail(app)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Import routes
from .routes import *

# Main route
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('landing.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500 