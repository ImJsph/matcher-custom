# flask is for the frontend web application with request handling the http information and jsonify for returning a good format of the data 
from flask import Flask, request, jsonify
# cors allows for a communication between separate ports since we are using the python and react for this app. A bridge of sorts
from flask_cors import CORS
# fitz is a library that is able to extract text from pdfs. It takes the text from the user's resume
import fitz  # PyMuPDF
# re handles the regex part of filtering for the words that we want to either highlight or ignore
import re
# cosine similarity works in tandem with the embeddings by comparing 2 vectors and seeing what the match is like there. 
from sklearn.metrics.pairwise import cosine_similarity
# sentence-transformers is a Hugging Face library that lets us use BERT-like models to generate embeddings for text
from sentence_transformers import SentenceTransformer


### APP INITILIZATION + CORS ###

# initialize the Flask app
app = Flask(__name__)
# allow frontend (React) to communicate with this backend API
CORS(app)


### TEXT TOOLS ###

# normalize text: lowercase, remove punctuation/symbols, trim whitespace
def normalize_text(text):
   if not isinstance(text, str):
       return ""
   text = text.lower()
   text = re.sub(r"\W+", " ", text)
   return text.strip()

# extract text from uploaded resume PDF
def extract_resume_text(pdf_path):
   doc = fitz.open(pdf_path)
   return " ".join([page.get_text() for page in doc])


### BERT MODEL ###

# load pre-trained BERT sentence transformer
bert_model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")


### CUSTOM JOB DESCRIPTION MATCH ROUTE ###

@app.route("/match_custom", methods=["POST"])
def match_custom():
    try:
        # get resume from uploaded file
        file = request.files["resume"]
        file.save("uploaded_resume.pdf")
        resume_text = extract_resume_text("uploaded_resume.pdf")
        resume_text = normalize_text(resume_text)

        # get custom job description text from the request
        job_text = request.form.get("job_description", "")
        job_text = normalize_text(job_text)

        if not resume_text or not job_text:
            return jsonify({"error": "Missing resume or job description"}), 400

        # encode both resume and job description with BERT
        resume_embedding = bert_model.encode([resume_text], convert_to_numpy=True)
        job_embedding = bert_model.encode([job_text], convert_to_numpy=True)

        # compute similarity score
        score = float(cosine_similarity(resume_embedding, job_embedding)[0][0])

        # extract matched and suggested keywords
        resume_words = set(re.findall(r'\b\w+\b', resume_text))
        job_words = set(re.findall(r'\b\w+\b', job_text))
        matched_keywords = sorted(resume_words & job_words)[:10]   # cap at 10
        suggested_keywords = sorted(job_words - resume_words)[:10] # cap at 10

        print("✅ Custom job description matching complete.")

        return jsonify({
            "job_description": job_text,
            "match_score": score,
            "matched_keywords": matched_keywords,
            "suggested_keywords": suggested_keywords
        })

    except Exception as e:
        print("❌ Error in /match_custom:", str(e))
        return jsonify({"error": str(e)}), 500


# start running the flask app
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # use Render's PORT, fallback to 5001 locally
    app.run(debug=False, host="0.0.0.0", port=port)
