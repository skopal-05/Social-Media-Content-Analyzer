# Social Media Content Analyzer

A full-stack web application that analyzes social media content extracted from PDF and image files and provides engagement-focused insights and content improvement recommendations.

## Live Application

https://social-media-content-analyzer-q0rxpqpzp-kopal.vercel.app/

## Backend API

https://social-media-content-analyzer-joed.onrender.com

## API Documentation

https://social-media-content-analyzer-joed.onrender.com/docs

---

## Features

- PDF file upload
- JPG, JPEG, and PNG image upload
- Drag-and-drop file upload
- File picker support
- PDF text extraction using PyMuPDF
- OCR-based text extraction using Tesseract
- Scanned PDF processing
- Content quality analysis
- Engagement potential scoring
- Hook analysis
- Clarity analysis
- Call-to-action analysis
- Hashtag analysis
- Readability analysis
- AI-powered content analysis using Google Gemini
- Content strengths and weaknesses
- Actionable improvement suggestions
- Improved content generation
- Recommended tone
- Recommended content type
- Loading states
- Error handling
- Responsive user interface
- REST API using FastAPI

---

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- PyMuPDF
- Tesseract OCR
- Pytesseract
- Pillow
- Google Gemini API

### Deployment

- Vercel — Frontend
- Render — Backend
- Docker — Backend containerization

---

## Architecture

```text
                         User
                          |
                          v
                 React + Vite Frontend
                          |
                          | HTTP Requests
                          v
                   FastAPI Backend
                          |
              +-----------+-----------+
              |                       |
              v                       v
        PDF Text Extraction       Tesseract OCR
           (PyMuPDF)             (Images/Scans)
              |                       |
              +-----------+-----------+
                          |
                          v
                   Extracted Text
                          |
              +-----------+-----------+
              |                       |
              v                       v
       Rule-Based Analysis       Gemini AI
              |                       |
              +-----------+-----------+
                          |
                          v
                  Analysis Results
                          |
                          v
                    Frontend UI
```

---

## Application Flow

```text
1. User uploads a PDF or image
              |
              v
2. File validation
              |
              v
3. Text extraction
              |
       +------+------+
       |             |
     PDF           Image
       |             |
   PyMuPDF       Tesseract
       |             |
       +------+------+
              |
              v
4. Extracted text
              |
              v
5. Rule-based content analysis
              |
              v
6. Gemini AI analysis
              |
              v
7. Engagement insights
              |
              v
8. Improved content and recommendations
```

---

## Project Structure

```text
Social-Media-Content-Analyzer/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── pdf.py
│   │   │   └── image.py
│   │   │
│   │   ├── services/
│   │   │   ├── ai_analyzer.py
│   │   │   ├── analyzer.py
│   │   │   ├── ocr_service.py
│   │   │   └── pdf_extractor.py
│   │   │
│   │   ├── schemas.py
│   │   └── main.py
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health/status |
| POST | `/analyze/pdf` | Analyze PDF content |
| POST | `/analyze/image` | Analyze image content |

---

## PDF Analysis

The PDF endpoint supports both text-based and scanned PDFs.

### Text-Based PDF

```text
PDF
 |
 v
PyMuPDF
 |
 v
Extracted Text
 |
 v
Content Analysis
 |
 v
Gemini AI
 |
 v
Recommendations
```

### Scanned PDF

```text
Scanned PDF
 |
 v
PyMuPDF Page Rendering
 |
 v
Tesseract OCR
 |
 v
Extracted Text
 |
 v
Content Analysis
 |
 v
Gemini AI
 |
 v
Recommendations
```

---

## Image Analysis

Supported image formats:

```text
JPG
JPEG
PNG
```

Processing flow:

```text
Image
 |
 v
Tesseract OCR
 |
 v
Extracted Text
 |
 v
Rule-Based Analysis
 |
 v
Gemini AI Analysis
 |
 v
Recommendations
```

---

## Analysis Output

The application evaluates content using factors such as:

- Engagement potential
- Hook quality
- Clarity
- Call-to-action effectiveness
- Hashtag usage
- Readability
- Overall content quality

The AI analysis provides:

- Strengths
- Weaknesses
- Improvement suggestions
- Improved content version
- Recommended tone
- Recommended content type

### Example Response

```json
{
  "engagement_potential": 85,
  "strengths": [
    "Clear announcement format",
    "Direct call to action",
    "Relevant hashtags"
  ],
  "weaknesses": [
    "Limited product details",
    "Could provide a stronger value proposition"
  ],
  "suggestions": [
    "Add a key product benefit",
    "Use a stronger call to action"
  ],
  "improved_version": "Improved social media content...",
  "recommended_tone": "Conversational",
  "recommended_content_type": "Announcement"
}
```

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm
- Tesseract OCR
- Git

---

## Backend Setup

Navigate to the backend directory:

```powershell
cd backend
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the backend:

```powershell
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Open a new terminal and navigate to the frontend directory:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

---

## OCR Setup

The application uses Tesseract OCR for extracting text from:

- Images
- Scanned PDFs

Verify Tesseract installation:

```powershell
tesseract --version
```

The production backend installs Tesseract through its Docker image.

---

## Docker

The backend is containerized using Docker to provide a consistent production environment and system-level Tesseract OCR support.

Docker architecture:

```text
Python 3.11
    |
    +-- Tesseract OCR
    |
    +-- FastAPI
    |
    +-- PyMuPDF
    |
    +-- Pytesseract
    |
    +-- Google Gemini
```

Build the backend image:

```powershell
docker build -t social-media-content-analyzer ./backend
```

Run locally:

```powershell
docker run -p 8000:8000 --env-file backend/.env social-media-content-analyzer
```

---

## Deployment

### Frontend

The frontend is deployed using Vercel.

Live application:

https://social-media-content-analyzer-q0rxpqpzp-kopal.vercel.app/

Configuration:

```text
Platform: Vercel
Framework: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

### Backend

The backend is deployed using Render.

Live API:

https://social-media-content-analyzer-joed.onrender.com

Configuration:

```text
Platform: Render
Runtime: Docker
Root Directory: backend
```

The Docker image installs Tesseract OCR and the required Python dependencies before starting the FastAPI application.

---

## Error Handling

The application handles common errors including:

- Unsupported file formats
- Empty files
- Files exceeding the size limit
- Invalid PDF files
- Invalid image files
- Failed text extraction
- OCR failures
- AI service failures
- Invalid content
- Backend/API errors

AI analysis is treated as an enhancement. If the Gemini API is unavailable, the application can still return the rule-based analysis.

---

## Security

- API keys are stored using environment variables.
- Secrets are excluded from version control.
- API keys are not exposed in the frontend.
- Uploaded files are validated before processing.
- File size limits are enforced.
- CORS is configured for the deployed frontend.
- Production configuration is separated from local development configuration.

---

## Design Approach

The application follows a modular full-stack architecture.

```text
Frontend
   |
   +-- File Upload
   +-- User Interface
   +-- Loading States
   +-- Results Display
   |
Backend
   |
   +-- API Routes
   +-- PDF Extraction
   +-- OCR Processing
   +-- Rule-Based Analysis
   +-- AI Analysis
```

The separation of frontend, API routes, extraction services, OCR processing, and AI analysis makes the application easier to maintain and extend.

---

## Assessment Requirements

| Requirement | Implementation |
|-------------|----------------|
| PDF upload | Implemented |
| Image upload | Implemented |
| Drag-and-drop | Implemented |
| File picker | Implemented |
| PDF text extraction | PyMuPDF |
| OCR | Tesseract |
| AI analysis | Google Gemini |
| Engagement recommendations | Implemented |
| Loading states | Implemented |
| Error handling | Implemented |
| Documentation | README |

---

## Future Improvements

- Social-media-platform-specific optimization
- User authentication
- Analysis history
- Multiple file processing
- Exportable analysis reports
- Platform-specific hashtag recommendations
- A/B content comparison
- Analytics dashboard
