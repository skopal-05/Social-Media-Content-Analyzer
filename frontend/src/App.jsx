import { useRef, useState } from "react";
import {
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Clipboard,
  FileText,
  Image as ImageIcon,
  Loader2,
  Sparkles,
  Target,
  Upload,
  X,
} from "lucide-react";

import "./App.css";

const API_BASE_URL = "https://social-media-content-analyzer-joed.onrender.com";
const MAX_FILE_SIZE = 10 * 1024 * 1024;

const ACCEPTED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"];

function App() {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [showExtractedText, setShowExtractedText] = useState(false);

  const validateFile = (file) => {
    if (!file) return "Please select a file.";

    const extension = `.${file.name.split(".").pop().toLowerCase()}`;

    if (!ACCEPTED_EXTENSIONS.includes(extension)) {
      return "Please upload a PDF, JPG, JPEG, or PNG file.";
    }

    if (file.size > MAX_FILE_SIZE) {
      return "File size must be less than 10 MB.";
    }

    if (file.size === 0) {
      return "The selected file is empty.";
    }

    return "";
  };

  const handleFileSelection = (file) => {
    setError("");
    setResult(null);
    setCopied(false);

    const validationError = validateFile(file);

    if (validationError) {
      setSelectedFile(null);
      setError(validationError);
      return;
    }

    setSelectedFile(file);
  };

  const handleInputChange = (event) => {
    const file = event.target.files?.[0];

    if (file) {
      handleFileSelection(file);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);

    const file = event.dataTransfer.files?.[0];

    if (file) {
      handleFileSelection(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const removeFile = () => {
    setSelectedFile(null);
    setResult(null);
    setError("");
    setCopied(false);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const analyzeFile = async () => {
    if (!selectedFile) {
      setError("Please select a file first.");
      return;
    }

    setIsAnalyzing(true);
    setError("");
    setResult(null);
    setCopied(false);

    try {
      const extension = selectedFile.name
        .split(".")
        .pop()
        .toLowerCase();

      const formData = new FormData();
      formData.append("file", selectedFile);

      const endpoint =
        extension === "pdf"
          ? `${API_BASE_URL}/analyze/pdf`
          : `${API_BASE_URL}/analyze/image`;

      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      let data;

      try {
        data = await response.json();
      } catch {
        throw new Error("The server returned an invalid response.");
      }

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to analyze the uploaded file."
        );
      }

      setResult(data);
    } catch (err) {
      if (err instanceof TypeError) {
        setError(
          "Unable to connect to the backend. Make sure FastAPI is running on port 8000."
        );
      } else {
        setError(
          err.message || "Something went wrong while analyzing the file."
        );
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getAnalysis = () => {
    if (!result) return {};

    return result.analysis || result;
  };

  const analysis = getAnalysis();

  const aiAnalysis =
    analysis.ai_analysis ||
    result?.ai_analysis ||
    {};

  const hasAIAnalysis =
    aiAnalysis &&
    Object.keys(aiAnalysis).length > 0 &&
    aiAnalysis.engagement_potential !== undefined;

  const scores =
    analysis.scores ||
    result?.scores ||
    {};

  const engagementScore =
    aiAnalysis.engagement_potential ??
    analysis.engagement_score ??
    result?.engagement_score ??
    0;

  const strengths =
    aiAnalysis.strengths ||
    analysis.strengths ||
    [];

  const weaknesses =
    aiAnalysis.weaknesses ||
    analysis.weaknesses ||
    [];

  const suggestions =
    aiAnalysis.suggestions ||
    analysis.suggestions ||
    [];

  const improvedVersion =
    aiAnalysis.improved_version ||
    analysis.improved_version ||
    "";

  const recommendedTone =
    aiAnalysis.recommended_tone ||
    analysis.recommended_tone ||
    "";

  const recommendedContentType =
    aiAnalysis.recommended_content_type ||
    analysis.recommended_content_type ||
    "";

  const extractedText =
    result?.extracted_text ||
    analysis.extracted_text ||
    "";

  const filename =
    result?.filename ||
    selectedFile?.name ||
    "Uploaded file";

  const copyImprovedVersion = async () => {
    if (!improvedVersion) return;

    try {
      await navigator.clipboard.writeText(improvedVersion);
      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);
    } catch {
      setError("Unable to copy the improved version.");
    }
  };

  const analyzeAnother = () => {
    removeFile();

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const getFileIcon = () => {
    if (!selectedFile) {
      return <Upload size={28} />;
    }

    const extension = selectedFile.name
      .split(".")
      .pop()
      .toLowerCase();

    if (extension === "pdf") {
      return <FileText size={24} />;
    }

    return <ImageIcon size={24} />;
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="nav-inner">
          <div className="brand">
            <div className="brand-icon">
              <Sparkles size={19} />
            </div>

            <span>
              Content<span>Analyzer</span>
            </span>
          </div>

          <div className="nav-badge">AI-powered</div>
        </div>
      </header>

      <main>
        {!result && (
          <section className="hero">
            <div className="hero-badge">
              <Sparkles size={15} />
              Social Media Intelligence
            </div>

            <h1>
              Turn your content into
              <span> better engagement.</span>
            </h1>

            <p className="hero-description">
              Upload a PDF or image and get instant AI-powered insights,
              engagement recommendations, and an improved version of your
              content.
            </p>

            <div
              className={`upload-card ${
                isDragging ? "upload-card-dragging" : ""
              }`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={() =>
                !selectedFile && fileInputRef.current?.click()
              }
            >
              {!selectedFile ? (
                <>
                  <div className="upload-icon">
                    <Upload size={28} />
                  </div>

                  <h2>Drop your file here</h2>

                  <p>or click to browse from your computer</p>

                  <div className="file-types">
                    <span>PDF</span>
                    <span>JPG</span>
                    <span>PNG</span>
                    <span>Max 10 MB</span>
                  </div>
                </>
              ) : (
                <div className="selected-file">
                  <div className="selected-file-icon">
                    {getFileIcon()}
                  </div>

                  <div className="selected-file-info">
                    <strong>{selectedFile.name}</strong>

                    <span>
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>

                  <button
                    className="remove-file"
                    onClick={(event) => {
                      event.stopPropagation();
                      removeFile();
                    }}
                    type="button"
                  >
                    <X size={18} />
                  </button>
                </div>
              )}

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={handleInputChange}
                hidden
              />
            </div>

            {error && (
              <div className="error-message">
                <AlertCircle size={18} />
                <span>{error}</span>
              </div>
            )}

            {selectedFile && !isAnalyzing && (
              <button
                className="analyze-button"
                onClick={analyzeFile}
                type="button"
              >
                Analyze Content
                <ArrowRight size={19} />
              </button>
            )}

            {isAnalyzing && (
              <div className="loading-card">
                <div className="loading-icon">
                  <Loader2 size={25} className="spinner" />
                </div>

                <div>
                  <strong>Analyzing your content...</strong>

                  <p>
                    Extracting text and generating engagement insights
                  </p>
                </div>
              </div>
            )}

            <div className="feature-row">
              <Feature
                icon={<Target size={18} />}
                title="Engagement Score"
                description="Measure content potential"
              />

              <Feature
                icon={<Sparkles size={18} />}
                title="AI Suggestions"
                description="Get actionable improvements"
              />

              <Feature
                icon={<CheckCircle2 size={18} />}
                title="Smart Rewrite"
                description="Improve your original post"
              />
            </div>
          </section>
        )}

        {result && (
          <section className="results-section">
            <div className="results-header">
              <div>
                <div className="hero-badge">
                  <CheckCircle2 size={15} />
                  Analysis complete
                </div>

                <h1>
                  Your content
                  <span> breakdown.</span>
                </h1>

                <p>
                  Here&apos;s what our analyzer found and how you can improve
                  your content.
                </p>
              </div>

              <button
                className="secondary-button"
                onClick={analyzeAnother}
                type="button"
              >
                Analyze another
              </button>
            </div>

            <div className="score-card">
              <div className="score-left">
                <div className="score-label">
                  ENGAGEMENT POTENTIAL
                </div>

                <div className="score-number">
                  {engagementScore}
                  <span>/100</span>
                </div>

                <p>
                  Based on content quality, structure, and engagement signals.
                </p>
              </div>

              <div className="score-ring">
                <div
                  className="score-ring-progress"
                  style={{
                    "--score": `${Math.min(
                      Math.max(Number(engagementScore), 0),
                      100
                    ) * 3.6}deg`,
                  }}
                >
                  <div className="score-ring-inner">
                    <Target size={22} />
                  </div>
                </div>
              </div>
            </div>

            <div className="section-title">
              <span>Content metrics</span>
            </div>

            <div className="metrics-grid">
              <MetricCard
                label="Hook"
                value={scores.hook ?? 0}
              />

              <MetricCard
                label="Clarity"
                value={scores.clarity ?? 0}
              />

              <MetricCard
                label="Call to action"
                value={
                  scores.call_to_action ??
                  scores.cta ??
                  0
                }
              />

              <MetricCard
                label="Hashtags"
                value={scores.hashtags ?? 0}
              />

              <MetricCard
                label="Readability"
                value={scores.readability ?? 0}
              />
            </div>

            {hasAIAnalysis && (
              <>
                <div className="section-title">
                  <span>AI insights</span>

                  <div className="ai-label">
                    <Sparkles size={14} />
                    Gemini AI
                  </div>
                </div>

                <div className="insights-grid">
                  <InsightCard
                    title="Strengths"
                    icon="✓"
                    items={strengths}
                    type="positive"
                  />

                  <InsightCard
                    title="Areas to improve"
                    icon="!"
                    items={weaknesses}
                    type="warning"
                  />
                </div>

                <div className="suggestions-card">
                  <div className="card-heading">
                    <div className="card-heading-icon">
                      <Sparkles size={18} />
                    </div>

                    <div>
                      <h3>Actionable suggestions</h3>

                      <p>
                        Practical ways to increase engagement.
                      </p>
                    </div>
                  </div>

                  <div className="suggestions-list">
                    {suggestions.map((suggestion, index) => (
                      <div className="suggestion" key={index}>
                        <span>{index + 1}</span>
                        <p>{suggestion}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}

            <div className="section-title">
              <span>Recommended content</span>
            </div>

            <div className="rewrite-card">
              <div className="card-heading">
                <div className="card-heading-icon">
                  <Sparkles size={18} />
                </div>

                <div>
                  <h3>Improved version</h3>

                  <p>
                    A more engaging version of your original content.
                  </p>
                </div>
              </div>

              <div className="rewrite-content">
                {improvedVersion ||
                  "No improved version was generated for this file."}
              </div>

              <div className="rewrite-footer">
                <div className="recommendation-tags">
                  {recommendedTone && (
                    <span>
                      Tone: <strong>{recommendedTone}</strong>
                    </span>
                  )}

                  {recommendedContentType && (
                    <span>
                      Type:{" "}
                      <strong>{recommendedContentType}</strong>
                    </span>
                  )}
                </div>

                <button
                  className="copy-button"
                  onClick={copyImprovedVersion}
                  type="button"
                  disabled={!improvedVersion}
                >
                  {copied ? (
                    <>
                      <CheckCircle2 size={17} />
                      Copied
                    </>
                  ) : (
                    <>
                      <Clipboard size={17} />
                      Copy
                    </>
                  )}
                </button>
              </div>
            </div>

            <div className="section-title">
              <span>Extracted content</span>
            </div>

            <div className="extracted-card">
              <button
                className="extracted-toggle"
                onClick={() =>
                  setShowExtractedText(!showExtractedText)
                }
                type="button"
              >
                <div>
                  <FileText size={18} />
                  <span>{filename}</span>
                </div>

                {showExtractedText ? (
                  <ChevronUp size={18} />
                ) : (
                  <ChevronDown size={18} />
                )}
              </button>

              {showExtractedText && (
                <div className="extracted-text">
                  {extractedText || "No extracted text available."}
                </div>
              )}
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        <p>Social Media Content Analyzer</p>
        <span>Built with React, FastAPI & AI</span>
      </footer>
    </div>
  );
}

function Feature({ icon, title, description }) {
  return (
    <div className="feature">
      <div className="feature-icon">{icon}</div>

      <div>
        <strong>{title}</strong>
        <span>{description}</span>
      </div>
    </div>
  );
}

function MetricCard({ label, value }) {
  const safeValue = Math.min(Math.max(Number(value) || 0, 0), 10);

  return (
    <div className="metric-card">
      <span className="metric-label">{label}</span>

      <strong>
        {safeValue}
        <small>/10</small>
      </strong>

      <div className="metric-bar">
        <div style={{ width: `${safeValue * 10}%` }} />
      </div>
    </div>
  );
}

function InsightCard({ title, icon, items, type }) {
  return (
    <div className={`insight-card insight-${type}`}>
      <div className="insight-heading">
        <div className="insight-icon">{icon}</div>

        <h3>{title}</h3>
      </div>

      <div className="insight-list">
        {items.length > 0 ? (
          items.map((item, index) => (
            <div className="insight-item" key={index}>
              <span />
              <p>{item}</p>
            </div>
          ))
        ) : (
          <div className="insight-item">
            <span />
            <p>No items available.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;