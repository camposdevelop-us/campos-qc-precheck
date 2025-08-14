// let uploadedFileName = '';

// document.getElementById('runBtn').disabled = true; // Initially disable the Run button

// document.getElementById('fileInput').addEventListener('change', function(event) {
//     const file = event.target.files[0];
//     const preview = document.getElementById('pdfPreview');
//     if (file && file.type === 'application/pdf') {
//         const fileURL = URL.createObjectURL(file);
//         preview.src = fileURL;
//         document.getElementById('runBtn').disabled = false; // Enable Run button
//     } else {
//         preview.src = '';
//         document.getElementById('runBtn').disabled = true; // Disable Run button if not a PDF
//     }
// });

// document.getElementById('uploadForm').onsubmit = async function(e) {
//     e.preventDefault();
//     const formData = new FormData(e.target);
//     console.log(formData)
//     try {
//         // Use your FastAPI server URL here. If backend is on a different host/port, update this URL.
//         const res = await fetch('/analyze', {
//             method: 'POST',
//             body: formData
//         });
//         console.log(res)
//         // const data = await res.json();
//         // if (data.error) {
//         //     document.getElementById('result').innerText = "Error: " + data.error;
//         // } else {
//         //     uploadedFileName = data.filename;
//         //     document.getElementById('result').innerText = `Upload successful!`;
//         //     // Optionally display the analysis result immediately after upload (since it's processed at upload)
//         //     if (data.analysis) {
//         //         document.getElementById('analysisResult').innerText = `Analysis complete:\n${data.analysis}`;
//         //     } else {
//         //         document.getElementById('analysisResult').innerText = "";
//         //     }
//         // }
//     } catch (err) {
//         document.getElementById('result').innerText = "Upload failed.";
//     }
// };

// // Optional: keep this if you will later implement a separate "/analyze" backend route.
// // For now, since analysis is performed at upload, you may leave this as a no-op or display a message.
// document.getElementById('runBtn').onclick = async function() {
//     if (!uploadedFileName) return;
//     document.getElementById('analysisResult').innerText = "Analysis is now performed automatically when you upload a PDF.";
// };





document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const result = document.getElementById('result');
    const pdfPreview = document.getElementById('pdfPreview');
    const runBtn = document.getElementById('runBtn');

    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const fileURL = URL.createObjectURL(file);
        pdfPreview.src = fileURL;
        result.textContent = 'File uploaded successfully: ' + file.name;
        runBtn.style.display = 'block';
    } else {
        result.textContent = 'Please select a file to upload.';
    }
});

document.getElementById('runBtn').addEventListener('click', async function (e) {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const analysisResult = document.getElementById('analysisResult');
    analysisResult.textContent = 'Analysis is running... (this is a placeholder)';
    try {
        // Use your FastAPI server URL here. If backend is on a different host/port, update this URL.
        if (fileInput.files.length == 0) throw new Error("Please select any PDF file")
            const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file)
        console.log(formData)
        const res = await fetch('/analyze', {
            method: 'POST',
            body: formData
        }).then(res => res.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${file.name.split('.')[0]}.zip`
                document.body.appendChild(a);
                a.click();
                a.remove();
        });
        console.log(res)
        analysisResult.innerText = 'Analysis completed. Output file will be auto downloaded.'
        // const data = await res.json();
        // if (data.error) {
        //     document.getElementById('result').innerText = "Error: " + data.error;
        // } else {
        //     uploadedFileName = data.filename;
        //     document.getElementById('result').innerText = `Upload successful!`;
        //     // Optionally display the analysis result immediately after upload (since it's processed at upload)
        //     if (data.analysis) {
        //         document.getElementById('analysisResult').innerText = `Analysis complete:\n${data.analysis}`;
        //     } else {
        //         document.getElementById('analysisResult').innerText = "";
        //     }
        // }
    } catch (err) {
        analysisResult.innerText = "Analysis failed.";
    }
});