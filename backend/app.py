#Main entry point, creates flask app
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv() #loads env vars

app = Flask(__name__)
CORS(app)

port = int(os.getenv("PORT", 5000))

# import and register routes here
from routes.analysis_routes import analysis_bp #imports route file
app.register_blueprint(analysis_bp) #registers route file with flask

from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth") #in frontend we write auth/sigup etc

if __name__ == "__main__":
    app.run(debug=True, port=port)
