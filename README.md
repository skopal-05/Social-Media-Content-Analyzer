# Social Media Content Analyzer

An AI-powered web application that analyzes content extracted from PDF documents and images, evaluates its social media engagement potential, and provides actionable suggestions to improve the content.

The application supports both standard PDFs and scanned documents/images using text extraction and OCR, followed by AI-powered content analysis.

---

## Features

### 📄 Document Upload
- Upload PDF documents
- Upload JPG, JPEG, and PNG images
- Drag-and-drop support
- File picker support
- File size validation

### 🔍 Text Extraction
- Extract text from text-based PDFs
- Preserve readable document structure
- OCR support for scanned/image-based documents
- Tesseract-based text recognition for images and scanned PDFs

### 🤖 AI Content Analysis
The extracted content is analyzed using Google Gemini to generate:

- Engagement potential score
- Content strengths
- Areas for improvement
- Actionable suggestions
- Improved content version
- Recommended tone
- Recommended content type

### 📊 Content Metrics
The analyzer evaluates different content characteristics including:

- Hook
- Clarity
- Call-to-action
- Hashtags
- Readability

### 🎨 User Interface
- Clean and responsive React interface
- Drag-and-drop upload area
- Loading states
- Error handling
- Analysis dashboard
- Copy improved content functionality
- Expandable extracted text section
- Mobile-friendly layout

---

## Application Flow

```text
                  User
                   │
                   ▼
          Upload PDF / Image
                   │
                   ▼
            React Frontend
                   │
                   │ HTTP Request
                   ▼
             FastAPI Backend
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
     PDF Extraction       OCR
          │                 │
          └────────┬────────┘
                   ▼
             Extracted Text
                   │
                   ▼
              Gemini AI
                   │
                   ▼
          Content Analysis
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
     Score     Suggestions   Rewrite
                   │
                   ▼
             Results UI
```

---

## Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS
- Lucide React

### Backend
- Python
- FastAPI
- Uvicorn
- PyMuPDF
- Tesseract OCR
- Pillow

### AI
- Google Gemini API

### Deployment
- Frontend: Vercel
- Backend: Render

---

## Project Structure

```text
Social Media Content Analyzer/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── index.html
│
├── .gitignore
└── README.md
```

---

## Prerequisites

Make sure the following are installed:

- Python 3.10+
- Node.js 18+
- npm
- Git
- Tesseract OCR

A Google Gemini API key is also required for AI-powered analysis.

---

# Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/skopal-05/Social-Media-Content-Analyzer.git
cd Social-Media-Content-Analyzer
```

---

## 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

### Windows

```powershell
python -m venv ../venv
```

Activate it:

```powershell
..\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=your_gemini_model_here
```

Never commit the actual API key to GitHub.

The repository includes `.env.example` as a template.

---

## 4. Install Tesseract OCR

Tesseract OCR is required for scanned documents and image uploads.

After installing Tesseract, make sure it is available in your system PATH.

Verify the installation:

```powershell
tesseract --version
```

If the command is recognized, OCR is ready.

---

## 5. Run the Backend

From the `backend` directory:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Open a second terminal.

Navigate to the frontend:

```powershell
cd "E:\Projects\Social Media Content Analyzer\frontend"
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

## Frontend Environment Variable

For local development, create:

```text
frontend/.env
```

with:

```env
VITE_API_URL=http://127.0.0.1:8000
```

For production, this value should point to the deployed backend URL.

---

# API Endpoints

## PDF Analysis

```http
POST /analyze/pdf
```

Accepts a PDF file and:

1. Extracts text from the PDF.
2. Uses OCR when required.
3. Sends the extracted content for AI analysis.
4. Returns engagement metrics and recommendations.

---

## Image Analysis

```http
POST /analyze/image
```

Accepts:

- JPG
- JPEG
- PNG

The image is processed using OCR before AI analysis.

---

## Health Check

```http
GET /health
```

Used to verify that the backend service is running.

---

# Example Analysis

For uploaded content, the application can return information such as:

```json
{
  "engagement_potential": 85,
  "strengths": [
    "Clear announcement format",
    "Direct call to action"
  ],
  "weaknesses": [
    "Could include more specific details"
  ],
  "suggestions": [
    "Add a stronger value proposition",
    "Include a clear call-to-action"
  ],
  "improved_version": "Improved social media content...",
  "recommended_tone": "Conversational",
  "recommended_content_type": "Announcement"
}
```

---

# Error Handling

The application includes basic error handling for:

- Unsupported file formats
- Empty files
- Files larger than the allowed limit
- Failed text extraction
- OCR failures
- AI API failures
- Backend connection failures

The frontend displays appropriate loading and error states so users receive feedback during long-running operations.

---

# AI Analysis Approach

The application follows a simple content-analysis pipeline:

```text
Document
   ↓
Text Extraction / OCR
   ↓
Text Cleaning
   ↓
Gemini AI Analysis
   ↓
Structured Analysis
   ↓
Engagement Recommendations
```

The AI evaluates the content based on factors such as:

- Opening hook
- Clarity
- Engagement potential
- Call-to-action
- Hashtag usage
- Readability
- Overall content quality

It then produces actionable recommendations and an improved version of the content.

---

# Privacy & Security

- API credentials are stored in environment variables.
- `.env` files are excluded from Git.
- API keys are never required in the frontend.
- Uploaded files are processed by the backend for analysis.
- Sensitive documents should not be uploaded unnecessarily.
- Production deployments should use HTTPS and restricted CORS origins.

---

# Deployment

## Backend

The FastAPI backend can be deployed using services such as Render.

Recommended configuration:

```text
Root Directory:
backend

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Add the required environment variables in the hosting provider's dashboard.

---

## Frontend

The React/Vite frontend can be deployed using Vercel.

Recommended configuration:

```text
Root Directory:
frontend

Build Command:
npm run build

Output Directory:
dist
```

Set the production API URL:

```env
VITE_API_URL=https://your-backend-url
```

---

# Testing

The application was tested with:

- Text-based PDF documents
- Scanned PDF documents
- OCR-based extraction
- AI-generated engagement analysis
- AI-generated content improvements
- Invalid file handling
- Loading states
- Frontend-backend integration

---

# Future Improvements

Potential improvements include:

- User authentication
- Social media platform-specific scoring
- Instagram/LinkedIn/X post optimization
- Multiple file processing
- Analysis history
- Export analysis as PDF
- Advanced sentiment analysis
- Platform-specific hashtag recommendations
- Analytics dashboard
- Content comparison and A/B testing

---

# Assessment Requirements

This project addresses the requested technical assessment requirements:

| Requirement | Implementation |
|---|---|
| PDF upload | ✅ |
| Image upload | ✅ |
| Drag-and-drop | ✅ |
| File picker | ✅ |
| PDF text extraction | ✅ |
| OCR for scanned documents | ✅ |
| AI-powered analysis | ✅ |
| Engagement suggestions | ✅ |
| Loading states | ✅ |
| Error handling | ✅ |
| Production-quality structure | ✅ |
| Documentation | ✅ |

---

## Brief Approach

The application uses a two-stage processing pipeline. First, uploaded PDFs are processed using PDF text extraction, while scanned PDFs and image files are processed through OCR using Tesseract. The resulting text is normalized and sent to the backend AI analysis service. Google Gemini evaluates the content for engagement potential, clarity, hook quality, call-to-action effectiveness, readability, and hashtag usage. The model then generates strengths, weaknesses, actionable suggestions, an improved version, and recommended tone/content type. A FastAPI backend handles file processing and AI communication, while a React/Vite frontend provides a responsive interface with upload, loading, error, and results states. API credentials are stored securely through environment variables, and the application can be deployed using Render for the backend and Vercel for the frontend.

---