let uploadedFileName = '';

document.getElementById('runBtn').disabled = true; // Initially disable the Run button

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('pdfPreview');
    if (file && file.type === 'application/pdf') {
        const fileURL = URL.createObjectURL(file);
        preview.src = fileURL;
        document.getElementById('runBtn').disabled = false; // Enable Run button
    } else {
        preview.src = '';
        document.getElementById('runBtn').disabled = true; // Disable Run button if not a PDF
    }
});

document.getElementById('uploadForm').onsubmit = async function(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        // Use your FastAPI server URL here. If backend is on a different host/port, update this URL.
        const res = await fetch('http://localhost:8080/upload', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (data.error) {
            document.getElementById('result').innerText = "Error: " + data.error;
        } else {
            uploadedFileName = data.filename;
            document.getElementById('result').innerText = `Upload successful!`;
            // Optionally display the analysis result immediately after upload (since it's processed at upload)
            if (data.analysis) {
                document.getElementById('analysisResult').innerText = `Analysis complete:\n${data.analysis}`;
            } else {
                document.getElementById('analysisResult').innerText = "";
            }
        }
    } catch (err) {
        document.getElementById('result').innerText = "Upload failed.";
    }
};

// Optional: keep this if you will later implement a separate "/analyze" backend route.
// For now, since analysis is performed at upload, you may leave this as a no-op or display a message.
document.getElementById('runBtn').onclick = async function() {
    if (!uploadedFileName) return;
    document.getElementById('analysisResult').innerText = "Analysis is now performed automatically when you upload a PDF.";
};
