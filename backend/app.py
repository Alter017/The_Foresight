#Main entry point, creates flask app
from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS


load_dotenv() #loads env vars

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret_key")
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True

CORS(app)

port = int(os.getenv("PORT", 5000))

# import and register routes here -> if we dont register app.py will never know tht those routes exist
from routes.analysis_routes import analysis_bp #imports route file
app.register_blueprint(analysis_bp) #registers route file with flask

from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth") #in frontend we write auth/sigup etc

from routes.scenario_routes import scenario_bp
app.register_blueprint(scenario_bp, url_prefix="/scenario")

# from routes.preference_routes import preference_bp
# app.register_blueprint(preference_bp, url_prefix="/preference")


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True, port=port)
