# import json

# def get_ssl_grade(domain):
#     try:
#         # Example logic for SSL grade
#         grade = "A"
#         score_map = {"A+": 1.0, "A": 1.0, "B": 0.5, "C": 0.5, "D": 0.0}
#         score = score_map.get(grade, 0.0)

#         # Return as JSON string
#         return json.dumps({"score": score, "details": {"grade": grade}})
#     except Exception as e:
#         return json.dumps({"score": 0.0, "details": {"error": str(e)}})

# if __name__ == "__main__":
#     import sys
#     domain = sys.argv[1]
#     print(get_ssl_grade(domain))
import time
import sys
import requests
import json

def get_ssl_grade(domain):
    """
    Fetches the SSL grade for a given domain and returns a normalized score in JSON format:
    - Grade A+ or A → Score = 1.0
    - Grade B or C → Score = 0.5
    - Grade D or lower → Score = 0.0
    """
    url = f"https://api.ssllabs.com/api/v3/analyze?host={domain}&fromCache=on&startNew=off"
    grade_to_score = {"A+": 1.0, "A": 1.0, "B": 1.0, "C": 0.5, "D": 0.0}

    while True:
        try:
            response = requests.get(url).json()
            status = response.get("status")

            if status == "READY":
                grade = response["endpoints"][0].get("grade", "D")  # Default to "D" if grade is missing
                ssl_details = {
                    "grade": grade,
                    "status_message": "Analysis complete"
                }
                score = grade_to_score.get(grade, 0.0)
                return json.dumps({
                    "score": score,
                    "details": ssl_details
                })

            elif status == "ERROR":
                ssl_details = {"error": "Error in SSL Labs API analysis"}
                return json.dumps({
                    "score": 0.0,
                    "details": ssl_details
                })

            # Wait and retry if analysis is in progress
            time.sleep(10)

        except Exception as e:
            ssl_details = {"error": f"An exception occurred: {str(e)}"}
            return json.dumps({
                "score": 0.0,
                "details": ssl_details
            })

if __name__ == "__main__":
    if len(sys.argv) > 1:
        domain = sys.argv[1]
        print(get_ssl_grade(domain))
    else:
        # Provide a helpful error message if no domain is provided
        print(json.dumps({
            "score": 0.0,
            "details": {"error": "No domain provided. Usage: python script.py <domain>"}
        }))
