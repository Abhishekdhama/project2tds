import os
import json
from fastapi import FastAPI, File, UploadFile  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from dotenv import load_dotenv  # type: ignore
import openai  # type: ignore

load_dotenv()

app = FastAPI()

# Enable CORS (for testing purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("API key is missing. Make sure it's set in your .env file.")

openai.api_key = OPENAI_API_KEY

# Load questions from the JSON file
with open("graded_assisgnment.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

@app.get("/questions")
def get_questions():
    return JSONResponse(content=questions)

@app.post("/generate_answer")
async def generate_answer(question: str):
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        answer = response.choices[0].message['content']
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"data/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return JSONResponse(content={"info": f"File '{file.filename}' uploaded successfully."})
