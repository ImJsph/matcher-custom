HOW TO RUN:

Backend (Flask)
cd backend
pip install -r requirements.txt
python app.py

Frontend (React)
cd frontend
npm install
npm start

Notes:
Make sure the Flask server is running before using the React app.
Update any API URL in the frontend (if not running on localhost or default ports).

RUNDOWN
1. User Interface (Frontend – React)

Upload Resume PDF
User selects and uploads a .pdf file.

handleFileChange()
Stores the selected file in React state for later use.

Click “Match Resume”
Triggers the upload and matching workflow.

2. Upload & Request Handling

handleUpload()

Packages the file into FormData.

Sends a POST request to the Flask backend at /match.

Waits for a JSON response containing match results and keyword suggestions.

3. Flask Backend API (Python)

Endpoint: /match

Processing Steps

Extracts text from the uploaded PDF.

Normalizes and cleans the text.

Encodes the resume using a BERT embedding model.

Compares the resume vector to precomputed job embeddings.

Response (JSON)

{
  "matches": [...],
  "matched_keywords": [...],
  "suggested_keywords": [...]
}

4. React Frontend (Post-Response)

Response Handling

res.data.matches → setResults()

res.data.matched_keywords → setMatched()

res.data.suggested_keywords → setSuggested()

Conditional Rendering

If results.length > 0:

Display Top Matches (job title, company, location, score, link)

Display Matched Keywords

Display Suggested Keywords

Else:

Show nothing or prompt for upload

5. Key Technologies

Frontend: React, Axios

Backend: Flask (Python)

Model: BERT (SentenceTransformers)

File Handling: PyMuPDF for PDF text extraction

Communication: RESTful JSON API

