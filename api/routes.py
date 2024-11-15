from api.index import app, mail, serializer
from flask import render_template, request, redirect, url_for, flash
import os

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html')
        
        user = User.objects(email=email).first()
        if user:
            user.password_hash = generate_password_hash(password)
            user.save()
            flash('Your password has been updated! Please login with your new password.', 'success')
            return redirect(url_for('login'))
    
    return render_template('reset_password.html')

def send_reset_email(user_email):
    token = serializer.dumps(user_email, salt='password-reset-salt')
    
    # Get domain from environment
    domain = os.getenv('VERCEL_URL', 'localhost:5000')
    protocol = 'https' if 'vercel.app' in domain else 'http'
    
    reset_url = f"{protocol}://{domain}/reset_password/{token}"
    
    msg = Message('Password Reset Request',
                 sender=app.config['MAIL_USERNAME'],
                 recipients=[user_email])
    
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg) 