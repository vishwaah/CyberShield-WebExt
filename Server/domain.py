import sys
import json
from datetime import datetime
from whoisapi import Client
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize WHOIS API client
API_KEY = os.getenv("WHOIS_APIKEY")
client = Client(api_key=API_KEY)

def calculate_age_score(created_date):
    """
    Calculates a score based on the domain age.
    - Age > 3 years: Score = 1
    - Age 1–3 years: Score = 0.5
    - Age < 1 year: Score = 0
    """
    try:
        created_date_obj = datetime.strptime(created_date, '%Y-%m-%dT%H:%M:%SZ')
        age_years = (datetime.now() - created_date_obj).days / 365
        if age_years > 3:
            return 1.0
        elif 1 <= age_years <= 3:
            return 0.5
        else:
            return 0.0
    except Exception as e:
        return 0.0  # Default to 0 if date parsing fails

def domain_age(domain):
    """
    Fetches the WHOIS data for a domain and calculates the domain age score.
    """
    try:
        # Fetch WHOIS raw data
        resp_str = client.raw_data(domain)
        resp_json = json.loads(resp_str)

        # Extract creation date
        created_date = resp_json.get('WhoisRecord', {}).get('registryData', {}).get('createdDate', 'N/A')

        # Calculate score
        if created_date != 'N/A':
            score = calculate_age_score(created_date)
        else:
            score = 0.0  # Default to 0 if creation date is unavailable

        # Return result
        return json.dumps({
            "score": score,
            "details": {
                "created_date": created_date
            }
        })

    except json.JSONDecodeError:
        return json.dumps({
            "score": 0.0,
            "details": {
                "error": "Failed to decode WHOIS API response as JSON."
            }
        })

    except Exception as e:
        return json.dumps({
            "score": 0.0,
            "details": {
                "error": str(e)
            }
        })

# Main execution
if __name__ == "__main__":
    try:
        domain = sys.argv[1]  # Get domain from command-line arguments
        result = domain_age(domain)
        print(result)
    except IndexError:
        print(json.dumps({
            "score": 0.0,
            "details": {
                "error": "Domain name is required as a command-line argument."
            }
        }))
