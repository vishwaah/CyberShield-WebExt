import os
import requests
import base64
import sys
import json
from dotenv import load_dotenv
# VirusTotal API Key
load_dotenv()
API_KEY = os.getenv("VIRUSTOTAL_APIKEY")
BASE_URL = 'https://www.virustotal.com/api/v3/urls/'

# Function to encode the URL to base64 as required by VirusTotal API
def encode_url(url):
    """
    Encodes the URL in base64 format as required by VirusTotal API.
    """
    try:
        encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        return encoded_url
    except Exception as e:
        raise ValueError(f"Error encoding URL: {e}")

# Function to check if the URL is blacklisted
def check_url_blacklist(url):
    """
    Checks if a given URL is flagged as malicious by VirusTotal.
    Returns:
        - JSON-formatted string with the score and details.
    """
    try:
        # Encode the URL
        encoded_url = encode_url(url)
        
        headers = {
            'x-apikey': API_KEY
        }

        # Send the GET request to the VirusTotal API
        response = requests.get(BASE_URL + encoded_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for malicious detections
            detections = data['data']['attributes']['last_analysis_stats']['malicious']
            total_engines = sum(data['data']['attributes']['last_analysis_stats'].values())

            # Construct the result dictionary
            result = {
                "score": 1.0 if detections == 0 else 0.0,
                "details": {
                    "malicious_detections": detections,
                    "total_engines": total_engines
                }
            }
            return json.dumps(result)  # Convert to JSON string
        else:
            # Handle API errors
            result = {
                "score": 0.0,
                "details": {
                    "error": f"VirusTotal API request failed. Status code: {response.status_code}",
                    "message": response.json().get("error", {}).get("message", "Unknown error")
                }
            }
            return json.dumps(result)  # Convert to JSON string

    except requests.RequestException as e:
        result = {
            "score": 0.0,
            "details": {
                "error": f"HTTP request error: {str(e)}"
            }
        }
        return json.dumps(result)  # Convert to JSON string
    except Exception as e:
        result = {
            "score": 0.0,
            "details": {
                "error": f"Unexpected error: {str(e)}"
            }
        }
        return json.dumps(result)  # Convert to JSON string

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python blackListStatus.py <url>"}))
        sys.exit(1)
    
    domain = sys.argv[1]
    result = check_url_blacklist(domain)
    print(result)
