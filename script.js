// Stores the uploaded file name for later use in analysis
let uploadedFileName = '';

// Callback for file input change event
// Previews the selected PDF and shows the Run Analysis button if valid
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
    alert('Only PDF format is supported. Please choose a valid PDF file');
  }
});

// Callback for upload form submission
// Uploads the selected PDF to the Flask backend and displays the result
document.getElementById('uploadForm').addEventListener('submit', async function(event) {
  const fileInput = document.getElementById('fileInput');
  const result = document.getElementById('result');
  const file = fileInput.files[0];

  // PDF validation before upload
  if (!file || file.type !== 'application/pdf') {
    alert('Only PDF format is supported. Please choose a valid PDF file.');
    event.preventDefault();
    return;
  }

  event.preventDefault();

  const formData = new FormData();
  formData.append('file', file);

  try {
    // Send file to Flask /upload endpoint
    const res = await fetch('/upload', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    uploadedFileName = data.filename;
    result.textContent = `Upload successful! Total pages: ${data.page_count}`;
  } catch (err) {
    // Handles upload failure (e.g., server not running or error)
    result.textContent = 'Upload failed.';
  }
});

// Callback for Run Analysis button click
// Sends the uploaded file name to Flask /analyze endpoint and displays the analysis result
document.getElementById('runBtn').addEventListener('click', async function() {
  const analysisResult = document.getElementById('analysisResult');
  const showChecklistBtn = document.getElementById('showChecklistBtn');
  const checklistResult = document.getElementById('checklistResult');
  if (!uploadedFileName) return;
  analysisResult.textContent = 'Analysis is running...';
  showChecklistBtn.style.display = 'none';
  checklistResult.style.display = 'none';
  try {
    // Send filename to Flask /analyze endpoint
    const res = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename: uploadedFileName })
    });
    const data = await res.json();
    analysisResult.textContent = `✅ Analysis complete:\n${data.analysis}`;
    // Show the checklist button after analysis
    showChecklistBtn.style.display = 'inline-block';
  } catch (err) {
    analysisResult.textContent = 'Analysis failed.';
    showChecklistBtn.style.display = 'none';
  }
});

// Show checklist.txt content when button is clicked
document.getElementById('showChecklistBtn').addEventListener('click', async function() {
  const checklistResult = document.getElementById('checklistResult');
  checklistResult.textContent = 'Loading checklist...';
  checklistResult.style.display = 'block';
  try {
    // Assumes checklist.txt is served at /uploads/<filename_stem>/checklist.txt
    const checklistUrl = `/uploads/${uploadedFileName.replace(/\.pdf$/i, '')}/checklist.txt`;
    const res = await fetch(checklistUrl);
    if (!res.ok) throw new Error('Checklist not found');
    const text = await res.text();
    checklistResult.textContent = text;
  } catch (err) {
    checklistResult.textContent = 'Checklist not found or not ready.';
  }
});


// Show secondary select when client is chosen
const clientSelect = document.getElementById('clientSelect');
const secondarySelect = document.getElementById('secondarySelect');
if (clientSelect && secondarySelect) {
  clientSelect.addEventListener('change', function () {
    if (clientSelect.value) {
      secondarySelect.style.display = 'block';
    } else {
      secondarySelect.style.display = 'none';
    }
  });
}

// Dynamically populate clientSelect in alphabetical order
document.addEventListener('DOMContentLoaded', function() {
  const clients = [
    { value: 'Xcel', text: 'Xcel' },
    { value: 'PGE', text: 'PGE (Place Holder)' },
    { value: 'SDGE', text: 'SDGE (Place Holder)' },
    { value: 'Duke', text: 'Duke (Place Holder)' },
    { value: 'Sempra', text: 'Sempra (Place Holder)' },
    { value: 'Campos', text: 'Campos (Place Holder)' },
    { value: 'Nisource', text: 'Nisource (Place Holder)' }
  ];
  clients.sort((a, b) => a.text.localeCompare(b.text));
  const clientSelect = document.getElementById('clientSelect');
  if (clientSelect) {
    clients.forEach(client => {
      const option = document.createElement('option');
      option.value = client.value;
      option.textContent = client.text;
      clientSelect.appendChild(option);
    });
  }
});

// (Optional) Show checklist group if needed in future
// const checklistGroup = document.querySelector('.checklist-group');
// checklistGroup.style.display = 'block';

// Removed unfinished/unused code for tertiarySelect