import os
import json
import requests
import PyPDF2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def parse_resume_to_features(file_stream):
    """
    Takes a file stream (PDF), extracts text, and uses an LLM (NVIDIA Nemotron Reasoning)
    via raw requests to map resume content to the 11 ML model features.
    """
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_stream)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    except Exception as e:
        return {"error": str(e)}

    if not text.strip():
        return {"error": "Could not extract text from PDF."}

    # Initialize NVIDIA endpoint
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return {"error": "NVIDIA_API_KEY not found in environment."}

    try:
        invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Merge instructions into the user prompt to match the exact user payload structure
        system_instructions = """
        You are an expert HR parser. Extract the following student features from the resume text provided.
        Return ONLY a JSON object (without markdown blocks like ```json). If a metric cannot be found or inferred confidently, return null for that key. Do NOT guess blindly, but DO infer 'gender' from names/pronouns, and 'specialisation' from degree/major.
        Keys to return:
        - "cgpa": (float, e.g., 8.5)
        - "tenth_percentage": (float)
        - "twelfth_percentage": (float)
        - "internships": (integer count, max 3)
        - "internships_list": (list of strings, exact titles or companies of the internships)
        - "projects": (integer count, max 3)
        - "projects_list": (list of strings, names or short descriptions of the projects)
        - "technical_skills": (integer 1-5, where 1=Beginner, 5=Expert based on tech keywords)
        - "communication_skills": (integer 1-5, based on leadership/soft skills keywords)
        - "backlogs": (integer count)
        - "work_experience": (string "Yes" or "No", based on full-time/part-time employment history)
        - "gender": (string "Male" or "Female", infer from name or pronouns. If unsure, null)
        - "specialisation": (string, one of: "Computer Science", "Information Technology", "Electronics", "Mechanical", "Others")
        
        RESUME TEXT:
        """

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": system_instructions + text[:8000]
                }
            ],
            "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
            "max_tokens": 1024,
            "reasoning_budget": 512,
            "stream": False,
            "temperature": 0.6,
            "top_p": 0.95
        }

        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        response_content = data['choices'][0]['message']['content'].strip()
        
        # Robustly extract JSON block in case the LLM includes conversational text
        import re
        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response_content.strip()
            
        features = json.loads(json_str)
        
        return {
            "success": True,
            "features": features
        }

    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse LLM response as JSON: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network Error: {str(e)}"}
    except Exception as e:
        return {"error": f"LLM API Error: {str(e)}"}
