#Blueprint: template of operations that can be registered with main flask app
from flask import Blueprint, request, jsonify 
from services.llm_service import generate_pros_cons

analysis_bp = Blueprint("analysis", __name__) #create bp object named analysis

@analysis_bp.route("/gen-pros-cons", methods=["GET"]) #creates route w path /test and method GET
def gen_pros_cons_route():
    data = request.get_json() 

    scenario = data.get("scenario")
    options = data.get("Options")

    if not scenario:
        return jsonify({"error": "Scenario is required"}), 400 #400 = bad request
    
    if not options or not isinstance(options, list): #Checking tht there is option and tht it is a list
        return jsonify({"error": "Options must be a non-empty list"}), 400
    
    result = generate_pros_cons(scenario, options)
    
    return jsonify(result)