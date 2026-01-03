import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import PyPDF2
import google.generativeai as genai
from werkzeug.utils import secure_filename

# ==============================
# CONFIG
# ==============================
load_dotenv()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"  # Enable demo mode if API quota exceeded

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# Use free-tier compatible model that works with your API key
model = genai.GenerativeModel("gemini-flash-latest")

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# ==============================
# HELPER FUNCTIONS
# ==============================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==============================
# PDF TEXT EXTRACTION
# ==============================
def extract_text_from_pdf(pdf_path):
    """Extract text from PDF with error handling"""
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            if len(reader.pages) == 0:
                raise ValueError("PDF has no pages")
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")

# ==============================
# GEMINI HELPERS
# ==============================
def parse_resume(resume_text):
    if DEMO_MODE:
        return """
**DEMO MODE - Sample Resume Analysis**

Skills Identified:
• Python, JavaScript, Java
• Flask, React, Node.js
• MySQL, MongoDB
• Git, Docker, AWS
• Machine Learning, Data Analysis

Experience:
• 3+ years in software development
• Full-stack development experience
• Agile methodology

Education:
• Bachelor's degree in Computer Science
• Relevant certifications

Tools & Technologies:
• IDEs: VS Code, PyCharm
• Version Control: Git, GitHub
• Cloud: AWS, Azure
"""
    
    prompt = f"""
You are an ATS resume parser.

Extract:
- Skills
- Experience
- Education
- Tools & technologies

Resume:
{resume_text}
"""
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            raise Exception("⚠️ API Quota Exceeded!\n\nYour Gemini API free tier limit has been reached.\n\nSolutions:\n1. Get a new API key from https://aistudio.google.com/apikey\n2. Wait for quota reset (usually 24 hours)\n3. Upgrade to paid plan\n4. Enable DEMO_MODE=true in .env file for testing")
        raise


def parse_job_description(jd_text):
    if DEMO_MODE:
        return """
**DEMO MODE - Sample Job Description Analysis**

Required Skills:
• Python, JavaScript
• Flask, React
• MySQL, MongoDB
• Git, Docker
• AWS/Cloud platforms
• Problem-solving skills

Responsibilities:
• Develop and maintain web applications
• Write clean, efficient code
• Collaborate with cross-functional teams
• Participate in code reviews
• Deploy and monitor applications

Qualifications:
• Bachelor's degree in Computer Science or related field
• 3+ years of software development experience
• Strong understanding of web technologies
• Experience with Agile methodologies
"""
    
    prompt = f"""
You are a job description parser.

Extract:
- Required skills
- Responsibilities
- Qualifications
- Preferred qualifications

Job Description:
{jd_text}
"""
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            raise Exception("⚠️ API Quota Exceeded!\n\nYour Gemini API free tier limit has been reached.\n\nSolutions:\n1. Get a new API key from https://aistudio.google.com/apikey\n2. Wait for quota reset (usually 24 hours)\n3. Upgrade to paid plan\n4. Enable DEMO_MODE=true in .env file for testing")
        raise


def ats_match(resume, jd):
    if DEMO_MODE:
        return """
**DEMO MODE - Sample ATS Evaluation**

🎯 **Match Percentage: 78%**

✅ **Matching Skills:**
• Python - Strong match
• JavaScript - Strong match  
• Flask - Exact match
• Git - Exact match
• AWS - Present in both
• Problem-solving - Demonstrated

❌ **Missing Critical Skills:**
• React - Required but not found in resume
• Docker - Mentioned in JD, enhance in resume
• CI/CD - Consider adding if you have experience

💪 **Strengths:**
• Strong programming foundation
• Relevant years of experience
• Full-stack development background
• Cloud platform experience
• Good technical skill diversity

📈 **Areas for Improvement:**
1. Add React.js experience prominently
2. Include specific AWS services used
3. Add metrics/achievements to experience
4. Include relevant project examples
5. Add any Agile/Scrum certifications

🔑 **Keywords to Optimize:**
• React, Redux
• Microservices
• CI/CD Pipeline
• Unit Testing
• RESTful APIs
• Docker/Kubernetes

📊 **Overall Assessment:**
Good candidate with solid foundation. Resume shows relevant experience and most required skills. Adding front-end framework experience (React) and containerization tools would significantly improve match score. Consider highlighting specific achievements with measurable impact.

**Recommendation:** Strong candidate - consider for interview with focus on React experience assessment.
"""
    
    prompt = f"""
You are an advanced Applicant Tracking System (ATS) analyzer.

Compare the resume and job description thoroughly.

Provide a structured analysis with:
1. **Match Percentage**: A number between 0-100
2. **Matching Skills**: List skills present in both resume and JD
3. **Missing Critical Skills**: Skills required in JD but missing in resume
4. **Strengths**: Strong points in the resume
5. **Areas for Improvement**: Specific suggestions to improve the match
6. **Keywords Optimization**: Suggest important keywords to add
7. **Overall Assessment**: Brief summary of candidacy

Format the response clearly with headings and bullet points.

Resume:
{resume}

Job Description:
{jd}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            raise Exception("⚠️ API Quota Exceeded!\n\nYour Gemini API free tier limit has been reached.\n\nSolutions:\n1. Get a new API key from https://aistudio.google.com/apikey\n2. Wait for quota reset (usually 24 hours)\n3. Upgrade to paid plan\n4. Enable DEMO_MODE=true in .env file for testing")
        raise Exception(f"Error analyzing with AI: {str(e)}")

# ==============================
# SERVE STATIC FILES
# ==============================
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(".", filename)

# ==============================
# API ENDPOINTS
# ==============================
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Validate file upload
        if "resume" not in request.files:
            return jsonify({"error": "Resume PDF is required", "success": False}), 400

        resume_file = request.files["resume"]
        job_desc = request.form.get("job_description", "").strip()

        # Validate inputs
        if not resume_file.filename:
            return jsonify({"error": "No file selected", "success": False}), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({"error": "Only PDF files are allowed", "success": False}), 400

        if not job_desc:
            return jsonify({"error": "Job description is required", "success": False}), 400
        
        if len(job_desc) < 50:
            return jsonify({"error": "Job description is too short. Please provide more details.", "success": False}), 400

        # Secure filename and save
        filename = secure_filename(resume_file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        resume_file.save(pdf_path)

        # Extract text from PDF
        resume_text = extract_text_from_pdf(pdf_path)
        
        if not resume_text or len(resume_text) < 100:
            os.remove(pdf_path)  # Clean up
            return jsonify({"error": "Could not extract sufficient text from PDF. Please ensure it's not an image-based PDF.", "success": False}), 400

        # Process with AI
        parsed_resume = parse_resume(resume_text)
        parsed_jd = parse_job_description(job_desc)
        ats_result = ats_match(parsed_resume, parsed_jd)

        # Clean up uploaded file
        try:
            os.remove(pdf_path)
        except:
            pass

        return jsonify({
            "success": True,
            "parsed_resume": parsed_resume,
            "parsed_job_description": parsed_jd,
            "ats_result": ats_result,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        app.logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({
            "error": f"An error occurred: {str(e)}",
            "success": False
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ATS Resume Analyzer",
        "demo_mode": DEMO_MODE
    })

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    app.run(debug=True, port=8080)
