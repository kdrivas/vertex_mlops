import functions_framework

import json
import requests
import google.auth
from google.auth.transport.requests import Request

# GCP Project and Endpoint details
PROJECT_ID = "275482249960"
LOCATION = "us-central1"
ENDPOINT_ID = "8346992000284753920"
ENDPOINT_URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}:predict"


def get_access_token():
    """Gets an OAuth 2.0 access token using Application Default Credentials."""
    credentials, _ = google.auth.default()
    credentials.refresh(Request())
    return credentials.token

@functions_framework.http
def predict(request):
    """Handles incoming requests and forwards them to Vertex AI."""
    try:
        data = request.get_json()
        if not data:
            return {"error": "No JSON payload provided"}, 400

        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # Make request to Vertex AI
        response = requests.post(ENDPOINT_URL, headers=headers, json=data)
        
        # Return Vertex AI response
        return {"predictions": response.json()["predictions"]}, response.status_code
    except:
        return "Error", 400
