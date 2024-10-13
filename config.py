from datetime import datetime,timedelta

class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'supersecretkey'
    SERVER_NAME = 'localhost:5000'
    APPLICATION_ROOT = '/'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_COOKIE_NAME = 'my_session'
    SESSION_COOKIE_PATH = '/'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_REFRESH_EACH_REQUEST = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=12)
    MAX_COOKIE_SIZE = 4093
    PROPAGATE_EXCEPTIONS = True
    TRAP_BAD_REQUEST_ERRORS = None
    TRAP_HTTP_EXCEPTIONS = False
    EXPLAIN_TEMPLATE_LOADING = False
    TEMPLATES_AUTO_RELOAD = True
    USE_X_SENDFILE = False
    PREFERRED_URL_SCHEME = 'https'
