let uploadedFileName = '';

document.getElementById('fileInput').addEventListener('change', function(event) {
  const file = event.target.files[0];
  const preview = document.getElementById('pdfPreview');
  const runBtn = document.getElementById('runBtn');

  if (file && file.type === 'application/pdf') {
    const fileURL = URL.createObjectURL(file);
    preview.src = fileURL;
    runBtn.style.display = 'block';
  } else {
    preview.src = '';
    runBtn.style.display = 'none';
  }
});

document.getElementById('uploadForm').addEventListener('submit', async function(event) {
  event.preventDefault();
  const fileInput = document.getElementById('fileInput');
  const result = document.getElementById('result');

  if (fileInput.files.length > 0) {
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
      const res = await fetch('/upload', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      uploadedFileName = data.filename;
      result.textContent = `Upload successful! Total pages: ${data.page_count}`;
    } catch (err) {
      result.textContent = 'Upload failed.';
    }
  } else {
    result.textContent = 'Please select a file to upload.';
  }
});

document.getElementById('runBtn').addEventListener('click', async function() {
  const analysisResult = document.getElementById('analysisResult');
  const loadingDots = document.getElementById('loadingDots');

  if (!uploadedFileName) return;

  analysisResult.textContent = 'Analysis is running...';
  loadingDots.style.display = 'block';

  try {
    const res = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename: uploadedFileName })
    });
    const data = await res.json();

    loadingDots.style.display = 'none';
    analysisResult.textContent = `✅ Analysis complete:\n${data.analysis}`;
  } catch (err) {
    loadingDots.style.display = 'none';
    analysisResult.textContent = 'Analysis failed.';
  }
});
