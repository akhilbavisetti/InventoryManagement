# Apply the HMAC patch for Python 3.13
import werkzeug_patch

from app import app

if __name__ == '__main__':
    app.run(debug=True) 