from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2
from docx import Document
import io

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Career Roadmap AI", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

# ==================== REQUEST MODELS ====================

class RoadmapRequest(BaseModel):
    role: str
    experience_level: str
    timeline_weeks: int
    learning_style: str

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_role: str = ""

class InterviewRequest(BaseModel):
    resume_text: str
    job_role: str
    difficulty: str

class FeedbackRequest(BaseModel):
    answer: str

# ==================== UTILITY FUNCTIONS ====================

def extract_text_from_pdf(pdf_bytes):
    """Extract text from PDF bytes"""
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def extract_text_from_docx(docx_bytes):
    """Extract text from DOCX bytes"""
    try:
        docx_file = io.BytesIO(docx_bytes)
        doc = Document(docx_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading DOCX: {str(e)}")

def generate_roadmap(role: str, experience_level: str, timeline_weeks: int, learning_style: str):
    """Generate roadmap using Gemini"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""Create a detailed learning roadmap for someone wanting to become a {role}.

User Details:
- Experience Level: {experience_level}
- Timeline: {timeline_weeks} weeks
- Learning Style: {learning_style}

Provide the roadmap in a clear, readable format. Include:
1. Prerequisites
2. Week-by-week topics with resources and projects
3. Skills to gain at each stage
4. Estimated salary range
5. Key milestones

Make it practical and actionable. Don't use JSON formatting - just present it in a clear, well-structured text format."""
    
    response = model.generate_content(prompt)
    return response.text

def analyze_resume(resume_text: str, job_role: str = ""):
    """Analyze resume using Gemini"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    job_context = f"for the {job_role} role" if job_role else ""
    
    prompt = f"""Analyze this resume {job_context} and provide a comprehensive evaluation:

RESUME:
{resume_text}

Please provide:
1. Overall Assessment (strengths and weaknesses)
2. ATS Compatibility Score (0-100) and why
3. Key Skills Identified
4. Missing Skills or Experience
5. Improvement Recommendations (specific and actionable)
6. Interview Readiness Score (0-100)

Format it in a clear, readable way. Be constructive and specific."""
    
    response = model.generate_content(prompt)
    return response.text

def generate_interview_questions(resume_text: str, job_role: str, difficulty: str):
    """Generate interview questions based on resume and job role"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    difficulty_guidance = {
        "Easy": "Basic questions about their experience and projects mentioned in the resume",
        "Medium": "Questions that require explanation of technical skills and decision-making",
        "Hard": "Challenging questions about complex scenarios, trade-offs, and deep technical knowledge"
    }
    
    prompt = f"""Generate 5 interview questions for a {job_role} position at {difficulty} difficulty level.

RESUME:
{resume_text}

Question Type: {difficulty_guidance[difficulty]}

For each question:
1. Ask a relevant question
2. Provide what would be a good answer
3. Provide tips for the candidate

Format each question clearly. Don't use JSON. Make it conversational and helpful."""
    
    response = model.generate_content(prompt)
    return response.text

def get_feedback(answer: str):
    """Get feedback on interview answer"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    feedback_prompt = f"""Based on the interview answer provided, give constructive feedback:

CANDIDATE'S ANSWER:
{answer}

Provide:
1. Strengths in the answer
2. Areas for improvement
3. Better way to answer
4. Rating (out of 10)

Be constructive and helpful."""
    
    response = model.generate_content(feedback_prompt)
    return response.text

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    return {"message": "Career Roadmap AI Backend", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/roadmap/generate")
async def roadmap_generate(request: RoadmapRequest):
    try:
        roadmap = generate_roadmap(
            request.role,
            request.experience_level,
            request.timeline_weeks,
            request.learning_style
        )
        return {"success": True, "data": roadmap}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resume/analyze")
async def resume_analyze(request: ResumeAnalysisRequest):
    try:
        analysis = analyze_resume(request.resume_text, request.job_role)
        return {"success": True, "data": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interview/generate")
async def interview_generate(request: InterviewRequest):
    try:
        questions = generate_interview_questions(
            request.resume_text,
            request.job_role,
            request.difficulty
        )
        return {"success": True, "data": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interview/feedback")
async def interview_feedback(request: FeedbackRequest):
    try:
        feedback = get_feedback(request.answer)
        return {"success": True, "data": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resume/upload")
async def resume_upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(contents)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(contents)
        else:
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        return {"success": True, "data": text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
