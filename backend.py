from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests

# Initialize FastAPI app
app = FastAPI()

# Define BlogRequest model
class BlogRequest(BaseModel):
    topic: str
    tone: str
    word_count: int

# Get API key from environment variable
API_KEY = os.getenv("AIzaSyCyaXNsU4XFg8SAZ3s3CWogx3-TL4gEsQQ")

if not API_KEY:
    raise ValueError("❌ API key not found. Set GEMINI_API_KEY in your environment variables.")

# Define the blog generation endpoint
@app.post("/generate")
async def generate_blog(request: BlogRequest):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": f"Write a {request.word_count}-word blog about '{request.topic}' in a {request.tone} tone."}]
        }]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])

            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                blog_content = parts[0].get("text", "") if parts else ""

                if blog_content:
                    return {"blog": blog_content}

            return {"error": "No content generated from Gemini API."}

        return {"error": f"Failed to fetch blog. Status Code: {response.status_code}, Message: {response.text}"}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling Gemini API: {str(e)}")
