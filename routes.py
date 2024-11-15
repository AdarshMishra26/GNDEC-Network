from api.index import app, mail, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, Post, Comment, FriendRequest
import cloudinary.uploader

# Copy all your route handlers here
@app.route('/')
def index():
    if current_user.is_authenticated:
        friend_ids = [friend.id for friend in current_user.friends]
        friend_ids.append(current_user.id)
        posts = Post.objects(user_id__in=friend_ids).order_by('-timestamp')
        return render_template('index.html', posts=posts)
    return render_template('landing.html')

# Add all other routes here... 