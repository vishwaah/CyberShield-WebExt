from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import subprocess
import json
import requests  # For URL validation

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500"]}})  # Enable CORS for all routes

def is_valid_url(url):
    """
    Validates if the given URL exists and is reachable.
    """
    try:
        response = requests.get(url,timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def run_script(script_name, arg):
    """
    Run a Python script with a URL argument and return the output.
    Expects the script to print a JSON-formatted string.
    """
    path = "C:\\Users\\rudra\\OneDrive\\Documents\\CyberShield-main[1]\\CyberShield-main\\server\\"
    try:
        result = subprocess.run(
            ['python', f'{path + script_name}.py', arg],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {
                "score": 0.0,
                "details": {
                    "error": f"Script {script_name} failed: {result.stderr.strip()}"
                }
            }
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "score": 0.0,
            "details": {
                "error": f"Script {script_name} returned invalid JSON: {result.stdout.strip()}"
            }
        }
    except Exception as e:
        return {
            "score": 0.0,
            "details": {
                "error": f"Error running {script_name}: {str(e)}"
            }
        }

@app.route('/api/check-url', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Validate if the URL exists
    if not is_valid_url(url):
        return jsonify({"error": "Invalid or unreachable URL"}), 400

    # Run the scripts
    results = {
        "blackListStatus": run_script("blackListStatus", url),
        "domain": run_script("domain", url),
        "scrapingReviews": run_script("scrapingReviews", url),
        "socialMedia": run_script("socialMedia", url),
        "SSlGrade": run_script("SSlGrade", url)
    }

    # Calculate the final score
    final_score = sum(result["score"] for result in results.values() if "score" in result) / len(results)

    return jsonify({
        "final_score": final_score,
        "details": results
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
