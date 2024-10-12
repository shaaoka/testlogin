from google.oauth2 import id_token
from google.auth.transport import requests

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template


GOOGLE_OAUTH2_CLIENT_ID = ""



# def create_app(app_env=None):
def create_app():
    flask_app = Flask(__name__)
    return flask_app


app = create_app()


@app.route('/')
def index():
    return render_template('index.html', google_oauth2_client_id=GOOGLE_OAUTH2_CLIENT_ID)
    
@app.route('/google_sign_in', methods=['POST'])
def google_sign_in():
    try:
        # Get the token from the incoming request
        token = request.json.get('id_token')

        if not token:
            return jsonify({'error': 'Token missing'}), 400

        # Verify the token using Google's OAuth2 library
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_OAUTH2_CLIENT_ID)

        # Check if the token's audience matches your client ID
        if idinfo['aud'] != GOOGLE_OAUTH2_CLIENT_ID:
            return jsonify({'error': 'Invalid audience'}), 403

        # Optionally, verify domain if using Google Workspace
        # if 'hd' in idinfo and idinfo['hd'] != 'your-domain.com':
        #     return jsonify({'error': 'Invalid domain'}), 403

        # Extract user information (Google Account ID, email, etc.)
        userid = idinfo['sub']
        email = idinfo['email']

        # Here you can handle user authentication logic (e.g., creating a new user or logging in)
        return jsonify({'userid': userid, 'email': email}), 200

    except ValueError as e:
        # Invalid token or other verification issues
        return jsonify({'error': str(e)}), 400
  

# @app.route('/google_sign_in', methods=['POST'])
# def google_sign_in():
#     token = request.json['id_token']
#     print('token' + token)
#     try:
#         # Specify the GOOGLE_OAUTH2_CLIENT_ID of the app that accesses the backend:
#         id_info = id_token.verify_oauth2_token(
#             token,
#             requests.Request(),
#             GOOGLE_OAUTH2_CLIENT_ID
            
#         )

#         if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#             raise ValueError('Wrong issuer.')

#         # ID token is valid. Get the user's Google Account ID from the decoded token.
#         # user_id = id_info['sub']
#         # reference: https://developers.google.com/identity/sign-in/web/backend-auth
#     except ValueError:
#         # Invalid token
#         raise ValueError('Invalid token')
 
#     print('登入成功')
#     return jsonify({}), 200

@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(
        port=8080,
        use_reloader=True
        )