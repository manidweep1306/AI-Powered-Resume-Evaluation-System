// ==============================
// STATE MANAGEMENT
// ==============================
let currentAnalysis = null;
let isDemoMode = false;

// ==============================
// DOM ELEMENTS
// ==============================
const elements = {
    form: document.getElementById("atsForm"),
    resumeInput: document.getElementById("resume"),
    jobDescInput: document.getElementById("jobDescription"),
    loading: document.getElementById("loading"),
    result: document.getElementById("result"),
    errorMessage: document.getElementById("errorMessage"),
    errorText: document.getElementById("errorText"),
    charCount: document.getElementById("charCount"),
    fileName: document.querySelector(".file-name"),
    fileSize: document.querySelector(".file-size"),
    downloadBtn: document.getElementById("downloadBtn"),
    newAnalysisBtn: document.getElementById("newAnalysisBtn"),
    timestamp: document.getElementById("timestamp"),
    demoBanner: document.getElementById("demoBanner")
};

// Check if demo mode banner should be shown
window.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("http://127.0.0.1:8080/health");
        const data = await response.json();
        if (data.demo_mode) {
            isDemoMode = true;
            elements.demoBanner.classList.remove("hidden");
        }
    } catch (err) {
        console.log("Could not check demo mode status");
    }
});

// ==============================
// FILE INPUT HANDLER
// ==============================
elements.resumeInput.addEventListener("change", function() {
    const file = this.files[0];
    if (file) {
        elements.fileName.textContent = file.name;
        const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
        elements.fileSize.textContent = `(${sizeInMB} MB)`;
        
        // Validate file size
        if (file.size > 10 * 1024 * 1024) {
            showError("File size exceeds 10MB limit");
            this.value = "";
            elements.fileName.textContent = "No file selected";
            elements.fileSize.textContent = "";
        }
    } else {
        elements.fileName.textContent = "No file selected";
        elements.fileSize.textContent = "";
    }
});

// ==============================
// CHARACTER COUNTER
// ==============================
elements.jobDescInput.addEventListener("input", function() {
    const count = this.value.length;
    elements.charCount.textContent = count;
    
    if (count < 50 && count > 0) {
        elements.charCount.style.color = "#f44336";
    } else if (count >= 50) {
        elements.charCount.style.color = "#4CAF50";
    }
});

// ==============================
// TAB SWITCHING
// ==============================
const tabButtons = document.querySelectorAll(".tab-btn");
const tabContents = document.querySelectorAll(".tab-content");

tabButtons.forEach(button => {
    button.addEventListener("click", () => {
        const tabName = button.dataset.tab;
        
        // Remove active class from all tabs
        tabButtons.forEach(btn => btn.classList.remove("active"));
        tabContents.forEach(content => content.classList.remove("active"));
        
        // Add active class to clicked tab
        button.classList.add("active");
        document.getElementById(`${tabName}-tab`).classList.add("active");
    });
});

// ==============================
// FORM SUBMISSION
// ==============================
elements.form.addEventListener("submit", async function(e) {
    e.preventDefault();
    
    // Hide previous results and errors
    elements.result.classList.add("hidden");
    elements.errorMessage.classList.add("hidden");
    
    // Validate inputs
    const resume = elements.resumeInput.files[0];
    const jobDesc = elements.jobDescInput.value.trim();
    
    if (!resume) {
        showError("Please select a resume PDF file");
        return;
    }
    
    if (jobDesc.length < 50) {
        showError("Job description must be at least 50 characters");
        return;
    }
    
    // Prepare form data
    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDesc);
    
    // Show loading
    elements.loading.classList.remove("hidden");
    
    try {
        const response = await fetch("http://127.0.0.1:8080/analyze", {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok || !data.success) {
            throw new Error(data.error || "Analysis failed");
        }
        
        // Store current analysis
        currentAnalysis = data;
        
        // Display results
        displayResults(data);
        
    } catch (err) {
        console.error("Error:", err);
        showError(err.message || "Failed to connect to server. Please ensure the backend is running.");
    } finally {
        elements.loading.classList.add("hidden");
    }
});

// ==============================
// MARKDOWN TO HTML CONVERTER
// ==============================
function markdownToHtml(text) {
    if (!text) return '';
    
    // Convert headers
    text = text.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    text = text.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    text = text.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    // Convert bold
    text = text.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
    
    // Convert bullet lists
    text = text.replace(/^\*   (.+)$/gim, '<li>$1</li>');
    text = text.replace(/^\* (.+)$/gim, '<li>$1</li>');
    text = text.replace(/^• (.+)$/gim, '<li>$1</li>');
    text = text.replace(/^- (.+)$/gim, '<li>$1</li>');
    
    // Wrap consecutive list items in ul tags
    text = text.replace(/(<li>.*<\/li>\n?)+/g, function(match) {
        return '<ul>' + match + '</ul>';
    });
    
    // Convert horizontal rules
    text = text.replace(/^---$/gim, '<hr>');
    
    // Convert tables (basic support)
    text = text.replace(/\|(.+)\|/g, function(match) {
        const cells = match.split('|').filter(cell => cell.trim());
        return '<tr>' + cells.map(cell => '<td>' + cell.trim() + '</td>').join('') + '</tr>';
    });
    text = text.replace(/(<tr>.*<\/tr>\n?)+/g, function(match) {
        return '<table>' + match + '</table>';
    });
    
    // Convert line breaks to paragraphs
    text = text.split('\n\n').map(para => {
        if (!para.startsWith('<') && para.trim() !== '') {
            return '<p>' + para + '</p>';
        }
        return para;
    }).join('\n');
    
    // Convert single line breaks to <br>
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// ==============================
// DISPLAY RESULTS
// ==============================
function displayResults(data) {
    // Populate result fields with markdown rendering
    document.getElementById("parsedResume").innerHTML = markdownToHtml(data.parsed_resume);
    document.getElementById("parsedJD").innerHTML = markdownToHtml(data.parsed_job_description);
    document.getElementById("atsResult").innerHTML = markdownToHtml(data.ats_result);
    
    // Format and display timestamp
    if (data.timestamp) {
        const date = new Date(data.timestamp);
        elements.timestamp.textContent = date.toLocaleString();
    }
    
    // Show results section with animation
    elements.result.classList.remove("hidden");
    elements.result.scrollIntoView({ behavior: "smooth", block: "start" });
    
    // Switch to ATS tab
    tabButtons[0].click();
}

// ==============================
// ERROR HANDLING
// ==============================
function showError(message) {
    elements.errorText.textContent = message;
    elements.errorMessage.classList.remove("hidden");
    elements.errorMessage.scrollIntoView({ behavior: "smooth" });
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        elements.errorMessage.classList.add("hidden");
    }, 5000);
}

// ==============================
// DOWNLOAD REPORT
// ==============================
elements.downloadBtn.addEventListener("click", function() {
    if (!currentAnalysis) return;
    
    const reportContent = `
ATS RESUME ANALYSIS REPORT
Generated: ${new Date().toLocaleString()}
${"=".repeat(60)}

RESUME ANALYSIS
${"-".repeat(60)}
${currentAnalysis.parsed_resume}

JOB DESCRIPTION ANALYSIS
${"-".repeat(60)}
${currentAnalysis.parsed_job_description}

ATS EVALUATION
${"-".repeat(60)}
${currentAnalysis.ats_result}

${"=".repeat(60)}
End of Report
`;
    
    const blob = new Blob([reportContent], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `ATS_Report_${new Date().getTime()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// ==============================
// NEW ANALYSIS
// ==============================
elements.newAnalysisBtn.addEventListener("click", function() {
    elements.result.classList.add("hidden");
    elements.form.reset();
    elements.fileName.textContent = "No file selected";
    elements.fileSize.textContent = "";
    elements.charCount.textContent = "0";
    currentAnalysis = null;
    window.scrollTo({ top: 0, behavior: "smooth" });
});