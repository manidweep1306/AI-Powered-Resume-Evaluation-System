# GenAI ATS Resume Analyzer

A professional, AI-powered Applicant Tracking System (ATS) resume analyzer built with Flask and Google Gemini AI.

## Features

- **PDF Resume Upload**: Upload resumes in PDF format for analysis
- **AI-Powered Analysis**: Leverages Google Gemini AI for intelligent resume evaluation
- **Match Scoring**: Get detailed match percentage between resume and job description
- **Skills Gap Analysis**: Identify missing skills and strengths
- **Interactive UI**: Modern, responsive interface with tabbed results
- **Download Reports**: Export analysis results as text files
- **Real-time Validation**: Input validation and error handling

## Technology Stack

- **Backend**: Flask (Python)
- **AI**: Google Gemini 1.5 Flash
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **PDF Processing**: PyPDF2
- **Styling**: Custom CSS with animations

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key

### Setup Steps

1. **Clone the repository** (or navigate to project directory)
   ```bash
   cd ats_gemini_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   - Open `.env` file
   - Replace with your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open browser and navigate to: `http://127.0.0.1:8080`

## Usage

1. **Upload Resume**: Click to select a PDF resume file (max 10MB)
2. **Enter Job Description**: Paste the complete job description (minimum 50 characters)
3. **Analyze**: Click the "Analyze Resume" button
4. **View Results**: Review the detailed analysis in three tabs:
   - ATS Evaluation: Match percentage and recommendations
   - Resume Analysis: Extracted skills and experience
   - Job Requirements: Parsed job description details
5. **Download**: Save the analysis report as a text file
6. **New Analysis**: Start fresh analysis with new documents

## Project Structure

```
ats_gemini_project/
├── app.py              # Flask backend application
├── index.html          # Main frontend page
├── script.js           # Frontend JavaScript logic
├── style.css           # Styling and animations
├── .env                # Environment variables (API keys)
├── requirements.txt    # Python dependencies
├── uploads/            # Temporary folder for PDF uploads
└── README.md           # Project documentation
```

## API Endpoints

### `POST /analyze`
Analyzes resume against job description
- **Request**: multipart/form-data
  - `resume`: PDF file
  - `job_description`: string
- **Response**: JSON with analysis results

### `GET /health`
Health check endpoint
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
