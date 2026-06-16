from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2
from docx import Document
import io
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

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

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

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

class ResourceRequest(BaseModel):
    topic: str

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
    
    prompt = f"""Create a learning roadmap for {role} (Level: {experience_level}, Timeline: {timeline_weeks}w, Style: {learning_style}).

Include:
1. Prerequisites (2-3 items)
2. Phase breakdown (3-4 phases max)
3. Key skills per phase
4. Resources for each phase
5. Final projects
6. Salary range

Be concise and actionable."""
    
    response = model.generate_content(prompt)
    return response.text

def analyze_resume(resume_text: str, job_role: str = ""):
    """Analyze resume using Gemini"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    job_context = f"for {job_role}" if job_role else ""
    
    prompt = f"""Quick resume analysis {job_context}:

RESUME:
{resume_text}

Provide (be concise):
1. ATS Score (0-100)
2. Top 5 Strengths
3. Top 5 Gaps
4. 3 Quick fixes
5. Interview readiness (0-100)"""
    
    response = model.generate_content(prompt)
    return response.text

def generate_interview_questions(resume_text: str, job_role: str, difficulty: str):
    """Generate interview questions based on resume and job role"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""Generate 3 {difficulty.lower()} interview questions for {job_role} based on this resume:

{resume_text}

For each:
1. Question
2. Good answer (brief)
3. 1 tip

Keep it concise."""
    
    response = model.generate_content(prompt)
    return response.text

def get_feedback(answer: str):
    """Get feedback on interview answer"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""Quick feedback on this interview answer:

ANSWER:
{answer}

Provide (concise):
1. Strengths
2. Improvements
3. Rating (0-10)"""
    
    response = model.generate_content(prompt)
    return response.text

def get_learning_resources(topic: str):
    """Get learning resources using CrewAI and Serper"""
    try:
        search_tool = SerperDevTool()
        
        researcher = Agent(
            role='Research Analyst',
            goal='Find important resources such as links and tutorials.',
            backstory='You are a fantastic research analyst who provides working resources for every topic',
            llm='gemini-2.5-flash',
            tools=[search_tool],
            verbose=False
        )
        
        task = Task(
            description=f'Research about {topic} and provide resources such as YouTube links, tutorial links, or website links.',
            expected_output=f'Top resources for {topic}, only give working links',
            agent=researcher
        )
        
        crew = Crew(agents=[researcher], tasks=[task])
        result = crew.kickoff()
        
        return str(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting resources: {str(e)}")

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

@app.post("/api/resources/search")
async def resources_search(request: ResourceRequest):
    try:
        resources = get_learning_resources(request.topic)
        return {"success": True, "data": resources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== FOR PRODUCTION ====================
# Removed if __name__ block for Render compatibility
# Render will use: uvicorn backend_main:app --host 0.0.0.0 --port $PORT
