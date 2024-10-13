from flask import Flask, redirect, url_for, session, request,render_template,jsonify
import google.auth
from google.oauth2 import id_token
from google.auth.transport import requests
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 用于加密 session

# 设置 Google OAuth 2.0 的配置
CLIENT_ID = ''  # 替换为你的客户端 ID
CLIENT_SECRET = ''  # 替换为你的客户端密钥
REDIRECT_URI = 'http://localhost:8080/callback'
SCOPES = 'openid email profile'


@app.route('/')
def index():
    return redirect(url_for('home'))



@app.route('/login')
def login():
    # 生成 state
    state = os.urandom(16).hex()
    session['state'] = state

    # 构建授权 URL
    authorization_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"scope={SCOPES.replace(' ', '%20')}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"state={state}"
    )

    return redirect(authorization_url)


@app.route('/callback')
def callback():
    # 获取回调参数
    state = request.args.get('state')
    print('state: ',state)
    code = request.args.get('code')
    print('code: ',code)

    # 检查 state 是否一致
    if state != session['state']:
        return "Error: Invalid state parameter", 400

    # 使用授权码交换访问令牌
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=data)
    token_info = response.json()
     # 打印获取到的访问令牌和其他信息
    print("Access Token:", token_info.get('access_token'))
    print("Refresh Token:", token_info.get('refresh_token'))
    print("Token Type:", token_info.get('token_type'))
    print("Expires In:", token_info.get('expires_in'))

    # 可选：获取用户信息
    user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {
        'Authorization': f"Bearer {token_info.get('access_token')}"
    }
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    # 打印用户信息
    print("User Info:", user_info)

    # return user_info
    
    return render_template('home.html', user_info=user_info)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout', methods=['POST'])
def logout():
    # 1. 清除 Flask 会话
    session.clear()

    # 2. 可选：重定向到 Google 的登出页面
    # Google 并没有明确的登出回调机制，只是简单地从 Google 页面登出
    # google_logout_url = 'https://accounts.google.com/logout'

    # 3. 重定向到应用程序的主页或登录页面
    return redirect(url_for('home'))  # 'home' 是主页路由

if __name__ == '__main__':
    app.run(
        port=8080,
        debug='true'
        )

