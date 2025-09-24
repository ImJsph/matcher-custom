// this is a shortcut library which internally simplifies using react.
// is responsible for managing the state - state refers to how a component remembers data which can change over time
import { useState } from "react";
// used for managing http requests
import axios from "axios";

function App() {
  // useState hook to store the uploaded resume file for the user
  const [file, setFile] = useState(null);

  // state for storing the raw text of a custom job description typed/pasted by the user
  const [jobDescription, setJobDescription] = useState("");
  // state for storing the backend response when comparing resume ↔ custom job description
  const [customResult, setCustomResult] = useState(null);

  // triggered when a user selects a file. It updates file to be the uploaded PDF.
  const handleFileChange = (e) => {
    // save the uploaded file to local state
    setFile(e.target.files[0]);
  };

  // triggered when the user clicks the "Match with Custom Job" button
  const handleCustomUpload = async () => {
    // error handler if no resume is uploaded
    if (!file) return alert("Please upload a PDF resume.");
    // error handler if no job description text is pasted
    if (!jobDescription.trim()) return alert("Please paste a job description.");

    // creates form data with both resume and custom job description
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jobDescription);

    // post request to backend (/match_custom) for custom job matching
    try {
      const res = await axios.post("https://matcher-custom.onrender.com/match_custom", formData);
      // save backend response (match score + keywords) into state
      setCustomResult(res.data);
    } catch (err) {
      console.error(err);
      alert("There was an error matching your resume to the custom job description.");
    }
  };

  return (
    // creates a <div> (a container) with inline styling to add 40px of padding. 
    // This is the main wrapper for all UI elements in the component.
    <div style={{ padding: 40 }}>
      {/* creates our header */}
      <h1>Custom Job Description Match</h1>

      {/* file input for uploading the resume PDF */}
      <input type="file" accept="application/pdf" onChange={handleFileChange} />

      {/* textarea for the user to paste a job description (multi-line input) */}
      <textarea
        placeholder="Paste job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        rows={6}
        cols={60}
        style={{ display: "block", marginTop: 10, marginBottom: 10 }}
      />

      {/* button that triggers handleCustomUpload, sending both resume + job description to backend */}
      <button onClick={handleCustomUpload}>Match with Custom Job</button>

      {/* only render the results if customResult has been set */}
      {customResult && (
        <div style={{ marginTop: 20 }}>
          <h3>Custom Job Match</h3>
          {/* display the similarity score */}
          <p><strong>Match Score:</strong> {customResult.match_score.toFixed(3)}</p>
          {/* display matched keywords (common between resume and custom JD) */}
          <h4>Matched Keywords</h4>
          <p>{customResult.matched_keywords.join(", ")}</p>
          {/* display suggested keywords (present in JD but missing from resume) */}
          <h4>Suggested Keywords</h4>
          <p>{customResult.suggested_keywords.join(", ")}</p>
        </div>
      )}
    </div>
  );
}

export default App;
