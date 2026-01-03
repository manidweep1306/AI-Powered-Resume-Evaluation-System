# 🚀 ATS Resume Analyzer - AI-Powered Resume Evaluation System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An intelligent Applicant Tracking System (ATS) powered by Google Gemini AI that helps job seekers optimize their resumes for better job matches.**

[Demo](#demo) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [API Documentation](#api-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Demo Mode](#demo-mode)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

The **ATS Resume Analyzer** is a sophisticated web application that leverages Google's Gemini AI to provide comprehensive resume analysis. It helps job seekers understand how well their resume matches a specific job description, identifies skill gaps, and provides actionable recommendations to improve their chances of passing through Applicant Tracking Systems.

### Why This Tool?

- **Beat ATS Systems**: 75% of resumes are rejected by ATS before reaching human recruiters
- **Instant Feedback**: Get immediate analysis and actionable insights
- **AI-Powered**: Utilizes Google's advanced Gemini AI for intelligent evaluation
- **Free & Open Source**: No hidden costs, fully transparent

---

## ✨ Features

### 🎯 Core Functionality

- **📄 PDF Resume Upload**: Support for standard PDF resume formats (max 10MB)
- **🤖 AI-Powered Analysis**: Advanced resume evaluation using Google Gemini Flash model
- **📊 Match Scoring**: Detailed percentage match between resume and job requirements
- **🔍 Skills Gap Analysis**: Identify missing skills, strengths, and improvement areas
- **💡 Smart Recommendations**: Actionable suggestions to improve resume quality
- **📈 ATS Optimization**: Tips to make resumes ATS-friendly

### 🎨 User Experience

- **Modern UI**: Clean, professional interface with smooth animations
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Tabbed Results**: Organized display of analysis, resume parsing, and job requirements
- **Download Reports**: Export complete analysis as text files
- **Real-time Validation**: Input validation with helpful error messages
- **Demo Mode**: Test the application without API quota concerns

### 🔒 Security & Performance

- **Secure File Handling**: Automatic cleanup of uploaded files
- **CORS Enabled**: Secure cross-origin requests
- **Error Handling**: Comprehensive error management and user feedback
- **File Size Limits**: Protection against oversized uploads
- **Input Sanitization**: Secure filename handling

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **AI Model**: Google Gemini 1.5 Flash
- **PDF Processing**: PyPDF2 3.0.1
- **Environment Management**: python-dotenv 1.0.0
- **CORS**: Flask-CORS 4.0.0

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **JavaScript (ES6+)**: Asynchronous operations with Fetch API
- **Font Awesome**: Professional icons
- **Google Fonts**: Inter font family

### Development
- **Python**: 3.8+
- **Package Manager**: pip
- **Environment Variables**: .env file
- **API**: Google Generative AI SDK

---

## 📦 Prerequisites

Before installation, ensure you have:

- **Python 3.8 or higher** installed ([Download Python](https://www.python.org/downloads/))
- **Google Gemini API Key** ([Get API Key](https://aistudio.google.com/apikey))
- **pip** package manager (included with Python)
- **Git** (optional, for cloning)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/manidweep1306/ATS-working.git
cd ATS-working
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Create Environment File

Create a `.env` file in the project root directory:

```bash
GEMINI_API_KEY=your_actual_api_key_here
DEMO_MODE=false
```

### 2. Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Click **"Create API Key"**
3. Copy the generated key
4. Paste it in your `.env` file

### 3. Directory Setup

The `uploads/` directory will be created automatically when you run the application.

---

## 💻 Usage

### Starting the Application

```bash
python app.py
```

The server will start on `http://127.0.0.1:8080`

### Using the Interface

1. **Upload Resume**
   - Click the upload area or drag & drop your PDF resume
   - Maximum file size: 10MB
   - Supported format: PDF only

2. **Enter Job Description**
   - Paste the complete job description in the text area
   - Minimum 50 characters required
   - Include skills, requirements, and responsibilities

3. **Analyze**
   - Click the **"Analyze Resume"** button
   - Wait for AI processing (typically 5-10 seconds)

4. **Review Results**
   - **ATS Evaluation Tab**: Match score and recommendations
   - **Resume Analysis Tab**: Parsed skills, experience, and education
   - **Job Requirements Tab**: Extracted job requirements and keywords

5. **Download Report**
   - Click **"Download Report"** to save analysis as a text file

6. **New Analysis**
   - Click **"New Analysis"** to start over

---

## 📁 Project Structure

```
ATS-working/
│
├── app.py                  # Flask backend application
├── index.html              # Main HTML interface
├── script.js               # Frontend JavaScript logic
├── style.css               # Styling and animations
│
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore file
│
├── README.md              # Project documentation
├── API_QUOTA_GUIDE.md     # API quota management guide
│
├── uploads/               # Temporary PDF storage (auto-created)
└── .venv/                 # Virtual environment (auto-created)
```

---

## 📡 API Documentation

### Endpoints

#### `POST /analyze`

Analyzes a resume against a job description.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `resume` (file): PDF file of the resume
  - `job_description` (string): Job description text

**Response:**
```json
{
  "success": true,
  "ats_score": "85%",
  "resume_analysis": "Detailed resume analysis...",
  "job_analysis": "Extracted job requirements...",
  "recommendations": "Actionable suggestions...",
  "demo_mode": false
}
```

#### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-03T10:30:00"
}
```

#### `GET /`

Serves the main HTML interface.

---

## 🎭 Demo Mode

When API quota is exhausted or for testing purposes, enable Demo Mode:

### Enable Demo Mode

In your `.env` file:
```
DEMO_MODE=true
```

### What Demo Mode Does

- ✅ Bypasses real API calls
- ✅ Returns realistic sample data
- ✅ Tests complete UI workflow
- ✅ No API quota consumption
- ✅ Banner notification for users

### Disable Demo Mode

Simply set `DEMO_MODE=false` or remove the line from `.env`

---

## 🔧 Troubleshooting

### Common Issues

#### **Issue**: Module not found errors
**Solution**: 
```bash
pip install -r requirements.txt --upgrade
```

#### **Issue**: API Quota Exceeded (429 Error)
**Solution**: 
- Enable Demo Mode temporarily
- Get a new API key from [Google AI Studio](https://aistudio.google.com/apikey)
- See [API_QUOTA_GUIDE.md](API_QUOTA_GUIDE.md) for detailed solutions

#### **Issue**: PDF not uploading
**Solution**: 
- Ensure file size is under 10MB
- Verify PDF is not password-protected
- Check file permissions

#### **Issue**: Port 8080 already in use
**Solution**: 
- Change port in `app.py`: `app.run(debug=True, host="0.0.0.0", port=5000)`
- Or kill the existing process using port 8080

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/YourFeature`
3. **Commit changes**: `git commit -m 'Add YourFeature'`
4. **Push to branch**: `git push origin feature/YourFeature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Test thoroughly before submitting PR
- Update documentation as needed

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini AI**: For providing powerful AI capabilities
- **Flask Community**: For the excellent web framework
- **Open Source Contributors**: For various libraries used

---

## 📞 Contact & Support

- **GitHub**: [@manidweep1306](https://github.com/manidweep1306)
- **Repository**: [ATS-working](https://github.com/manidweep1306/ATS-working)
- **Issues**: [Report a Bug](https://github.com/manidweep1306/ATS-working/issues)

---

## 🌟 Star This Repository

If you find this project helpful, please consider giving it a ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ by manidweep1306**

[⬆ Back to Top](#-ats-resume-analyzer---ai-powered-resume-evaluation-system)

</div>
- **Response**: JSON with service status

### `GET /`
Serves the main application page

## Configuration

### File Size Limits
- Maximum upload size: 10MB
- Adjust in `app.py`: `app.config["MAX_CONTENT_LENGTH"]`

### Supported File Types
- Currently supports: PDF only
- Modify `ALLOWED_EXTENSIONS` in `app.py` to add more types

## Deployment

### For Production

1. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8080 app:app
   ```

2. **Set environment variables**
   ```bash
   export GEMINI_API_KEY=your_api_key
   export FLASK_ENV=production
   ```

3. **Configure reverse proxy** (nginx/Apache) for better performance

4. **Enable HTTPS** using SSL certificates

5. **Set up monitoring** and logging

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
```

Build and run:
```bash
docker build -t ats-analyzer .
docker run -p 8080:8080 -e GEMINI_API_KEY=your_key ats-analyzer
```

## Troubleshooting

### Common Issues

1. **ImportError: Missing dependencies**
   - Solution: `pip install -r requirements.txt`

2. **API Key Error**
   - Solution: Verify `.env` file has correct GEMINI_API_KEY

3. **PDF extraction fails**
   - Solution: Ensure PDF is text-based, not image-based
   - Try OCR preprocessing for scanned PDFs

4. **Port already in use**
   - Solution: Change port in `app.py`: `app.run(port=5000)`

## Security Considerations

- API keys stored in `.env` (not committed to git)
- File size limits to prevent DoS attacks
- Secure filename handling with `werkzeug.secure_filename`
- Input validation for all user inputs
- Uploaded files are deleted after processing

## Performance Optimization

- Consider caching for repeated analyses
- Implement rate limiting for API endpoints
- Use CDN for static assets in production
- Optimize PDF parsing for large files

## Future Enhancements

- [ ] Support for multiple file formats (DOCX, TXT)
- [ ] User authentication and history tracking
- [ ] Batch processing of multiple resumes
- [ ] Advanced analytics and visualizations
- [ ] Email notifications for analysis completion
- [ ] API rate limiting and quotas
- [ ] Database integration for result storage

## License

This project is for educational and professional use.

## Support

For issues and questions:
- Check the troubleshooting section
- Review Flask and Gemini AI documentation
- Ensure all dependencies are up to date

## Credits

- Built with Flask and Google Gemini AI
- UI design inspired by modern web applications
- Icons from Font Awesome

---

**Version**: 1.0.0  
**Last Updated**: January 2, 2026  
**Status**: Production Ready ✅
