from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from dotenv import load_dotenv
import os
import cloudinary

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Configure app
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    MONGODB_SETTINGS={'host': os.getenv('MONGODB_URI')},
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS') == 'True',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
)

# Initialize extensions
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

mail = Mail(app)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Import routes after app initialization
from routes import *

# This is the handler Vercel will call
app = app 

if __name__ == '__main__': app.run()