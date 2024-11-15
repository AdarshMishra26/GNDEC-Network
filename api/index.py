from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, 
    logout_user, current_user, AnonymousUserMixin
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from mongoengine import *
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',  # Point to templates directory
           static_folder='../static')       # Point to static directory

# Configure app settings
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGODB_URI')
}

# Configure mail settings
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize extensions
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Import routes after app initialization
from routes import *

if __name__ == '__main__':
    app.run() 