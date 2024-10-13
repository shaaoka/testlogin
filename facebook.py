from flask import Flask, redirect, request, url_for, session
import requests

app = Flask(__name__)
app.secret_key = '4bcf3a2a7cd7c87f4a8b9329efa82ba2'

FB_CLIENT_ID = '3783385005234420'
FB_CLIENT_SECRET = 'your_fb_app_secret'
FB_REDIRECT_URI = 'https://yourdomain.com/auth/callback'

FB_AUTH_URL = 'https://www.facebook.com/v12.0/dialog/oauth'
FB_TOKEN_URL = 'https://graph.facebook.com/v12.0/oauth/access_token'
FB_API_URL = 'https://graph.facebook.com/me'

@app.route('/')
def index():
    return '<a href="/login">Login with Facebook</a>'

@app.route('/login')
def login():
    fb_login_url = (f"{FB_AUTH_URL}?client_id={FB_CLIENT_ID}&redirect_uri={FB_REDIRECT_URI}"
                    f"&state={session['state']}&scope=email")
    return redirect(fb_login_url)

@app.route('/auth/callback')
def callback():
    code = request.args.get('code')
    if code:
        token_response = requests.get(FB_TOKEN_URL, params={
            'client_id': FB_CLIENT_ID,
            'client_secret': FB_CLIENT_SECRET,
            'redirect_uri': FB_REDIRECT_URI,
            'code': code
        }).json()

        access_token = token_response['access_token']
        user_info = requests.get(FB_API_URL, params={
            'access_token': access_token,
            'fields': 'id,name,email'
        }).json()

        return f"Logged in as {user_info['name']} ({user_info['email']})"
    return 'Login failed'

if __name__ == '__main__':
    app.run(debug=True)
