# AI-Interview-Question-Generator-using-Transformers-BERT-T5


### Transformers • BERT • T5 • Hugging Face • Streamlit

An AI-powered interview preparation application that generates personalized interview questions based on a candidate's **role, skills, topics, or resume**. It uses **T5 for question generation** and **BERT for question ranking, duplicate removal, and answer evaluation**, with a Streamlit interface for interactive practice.

---

## 🚀 Features

### 1. Multiple Input Methods

The application supports three ways to generate interview questions:

* **Role + Skills**

  * Enter a target role and relevant skills.
  * Example: `AI Engineer`
  * Skills: `Python, Machine Learning, NLP, LLMs`

* **Single Topic**

  * Enter a specific topic to practice.
  * Example: `Transformers`

* **Resume Upload**

  * Upload a PDF resume.
  * The application extracts text from the resume.
  * Skills and project titles are identified from the extracted content.
  * Interview questions are generated based on the candidate's profile.

* **Resume Text**

  * Paste resume content directly into the application.

---

## 🎯 Interview Settings

Users can customize the generated questions using:

### Difficulty

* Beginner
* Intermediate
* Advanced

### Number of Questions

Choose how many questions should be generated for the practice session.

### Question Categories

Questions can be generated across multiple categories:

* Technical
* Coding
* Project
* HR

The application attempts to balance questions across selected skills and categories.

---

# 🧠 AI Pipeline

The application follows a multi-stage NLP pipeline.

```text
User Input
    │
    ▼
Role / Skills / Topic / Resume
    │
    ▼
Text Preprocessing
    │
    ▼
Skill & Project Extraction
    │
    ▼
Hugging Face Tokenizer
    │
    ▼
T5 Question Generation
    │
    ▼
Candidate Questions
    │
    ▼
BERT Semantic Ranking
    │
    ├── Duplicate Detection
    ├── Similarity Scoring
    └── Question Ranking
    │
    ▼
Skill & Category Balancing
    │
    ▼
Final Interview Questions
    │
    ▼
Practice & Answer Evaluation
```

---

# 🤖 Technologies Used

| Technology                | Purpose                            |
| ------------------------- | ---------------------------------- |
| Python                    | Application development            |
| Streamlit                 | Web interface                      |
| Hugging Face Transformers | NLP model integration              |
| T5 / FLAN-T5              | Question generation                |
| BERT                      | Semantic understanding and ranking |
| PyTorch                   | Deep learning backend              |
| PDF Processing            | Resume text extraction             |
| NLP                       | Skill and project extraction       |

---

# 🔥 Why T5 + BERT?

The application intentionally uses different Transformer models for different tasks.

### T5 — Question Generation

T5 is an encoder-decoder Transformer model capable of generating new text.

In this project, T5 is responsible for:

* Generating interview questions
* Creating questions from skills
* Generating topic-specific questions
* Producing variations of questions

Example:

```text
Input:
Python + Machine Learning + Intermediate

        ↓

T5

        ↓

"What is the difference between a list and a tuple in Python?"
```

### BERT — Understanding & Ranking

BERT is an encoder-only Transformer model.

It is used for:

* Semantic similarity
* Question ranking
* Near-duplicate detection
* Comparing questions
* Evaluating candidate answers

BERT **does not generate the questions**.

The architecture therefore separates the responsibilities:

```text
T5  → Generates questions
BERT → Understands, ranks & evaluates questions
```

This is an important concept to understand when explaining the project in an AI/ML interview.

---

# 📄 Resume Processing

When a resume is uploaded, the application performs several steps.

```text
Resume PDF
    ↓
Text Extraction
    ↓
Text Cleaning
    ↓
Section Identification
    ↓
Projects Section Extraction
    ↓
Skill Extraction
    ↓
Project Title Extraction
    ↓
Interview Question Generation
```

The system can use extracted:

* Technical skills
* Programming languages
* Frameworks
* Tools
* Project titles
* Project-related keywords

to personalize the interview questions.

---

# 📝 Question Generation

Questions are generated according to the selected:

* Role
* Skills
* Topic
* Resume
* Difficulty
* Category
* Number of questions

For example:

```text
Role:
AI Engineer

Skills:
Python, Machine Learning, NLP

Difficulty:
Advanced

Category:
Technical
```

The model can generate questions related to those requirements.

---

# 🧹 Question Filtering

Raw generated questions may contain:

* Duplicate questions
* Very similar questions
* Poorly formed questions
* Repeated concepts

BERT embeddings are used to identify semantically similar questions.

```text
Generated Question 1
Generated Question 2
Generated Question 3
Generated Question 4
        ↓
BERT Similarity
        ↓
Remove Near-Duplicates
        ↓
Rank Questions
        ↓
Final Question Set
```

This improves the variety of questions shown to the candidate.

---

# ⚖️ Skill & Category Balancing

The application attempts to avoid generating questions from only one skill.

For example, if the user selects:

```text
Python
Machine Learning
Deep Learning
NLP
```

the final question set can be distributed across those skills.

Similarly, when multiple categories are selected:

```text
Technical
Coding
Project
HR
```

the application attempts to maintain category diversity.

---

# 🎓 Practice Mode

The **Practice** tab allows users to answer generated questions.

The workflow is:

```text
Interview Question
       ↓
Candidate Answer
       ↓
Answer Analysis
       ↓
Concept Coverage
       ↓
Answer Length
       ↓
BERT Similarity
       ↓
Score / 100
       ↓
Missing Concepts
```

---

# 📊 Answer Evaluation

The answer score is an approximate practice score rather than a professional assessment.

The scoring combines multiple signals:

### Concept Coverage

Checks whether important concepts expected in the answer are present.

### Answer Length

Helps identify extremely short answers that may lack sufficient explanation.

### BERT Similarity

Measures semantic similarity between the candidate's answer and the expected/reference concepts.

The result is presented as:

```text
Score: 82 / 100

Missing Concepts:
- Cross-validation
- Overfitting
```

The score should be treated as **practice feedback**, not as a definitive measure of interview performance.

---

# 📥 Download Questions

Generated questions can be downloaded as a `.txt` file.

This allows users to:

* Save interview questions
* Practice offline
* Create personal question banks
* Share questions
* Prepare before interviews

---

# ⚡ Hugging Face Models

The application supports Hugging Face AI models.

Typical models include:

```text
FLAN-T5-Small
FLAN-T5-Base
BERT
```

### Model Size Considerations

The first run can take time because the models need to be downloaded and cached locally.

Approximate sizes can vary depending on the exact model and files downloaded.

A slower system may experience longer loading times.

After downloading, Hugging Face can load the models from the local cache.

---

# 📴 Offline / Lightweight Mode

The application includes a fallback mode for systems that cannot comfortably run Transformer models.

Disable:

```text
Use Hugging Face AI models
```

from the Streamlit sidebar.

The application then uses its built-in question bank.

This mode is useful when:

* Internet is unavailable
* Model downloads are too slow
* The laptop has limited RAM
* CPU inference is too slow
* You want to quickly test the application

The application also includes fallback behavior if model loading fails.

---

# 💻 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the repository URL with your GitHub repository URL.

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 🗂️ Project Structure

```text
AI-Interview-Question-Generator/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── run.bat
│
├── run.sh
│
├── .streamlit/
│   └── config.toml
│
└── assets/
    └── ...
```

### Main Files

**app.py**

Contains the Streamlit application, NLP pipeline, model loading, question generation, ranking and answer evaluation.

**requirements.txt**

Contains the Python dependencies required to run the project.

**.streamlit/config.toml**

Contains Streamlit configuration and UI theme settings.

**run.bat**

Windows helper script for starting the application.

**run.sh**

macOS/Linux helper script for starting the application.

**README.md**

Project documentation and setup instructions.

---

# ▶️ Quick Start — Windows

You can use:

```text
run.bat
```

or manually:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

# ▶️ Quick Start — macOS/Linux

```bash
chmod +x run.sh
./run.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

# ⚙️ Requirements

Recommended environment:

* Python 3.10+
* Internet connection for the first Hugging Face model download
* Sufficient RAM for Transformer models
* PyTorch-compatible environment

For limited-resource systems, use the built-in question-bank mode.

---

# ⚠️ Important Notes

### First Run

The first run may take longer because Hugging Face models need to be downloaded.

Do not close the application while the models are being loaded.

### Internet

Internet access is required for the initial model download unless the required models already exist in the local Hugging Face cache.

### CPU Systems

Transformer inference can be slower on CPU-only systems.

For faster generation, consider using a system with a compatible GPU.

### Generation Quality

Smaller models such as FLAN-T5-Small may occasionally generate simple, repetitive, or less natural questions.

FLAN-T5-Base can provide stronger generation quality but requires more computational resources.

---

# 🧪 Example Usage

### Example 1 — AI Engineer

```text
Role:
AI Engineer

Skills:
Python, Machine Learning, Deep Learning, NLP

Difficulty:
Advanced

Categories:
Technical, Coding, Project
```

Possible questions:

```text
Explain the difference between supervised and unsupervised learning.

How would you detect overfitting in a machine learning model?

Explain how attention mechanisms work in Transformers.

Describe an NLP project you have implemented and the challenges you faced.
```

---

### Example 2 — Python

```text
Topic:
Python

Difficulty:
Intermediate

Category:
Coding
```

The application generates Python-related interview questions and allows the candidate to practice answering them.

---

### Example 3 — Resume-Based Interview

```text
Upload Resume
       ↓
Extract Resume Text
       ↓
Identify Skills
       ↓
Identify Projects
       ↓
Generate Personalized Questions
       ↓
Practice Interview
```

This makes the questions more relevant to the candidate's own experience.

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      Streamlit      │
                    │      Interface      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   User Input Layer  │
                    │                     │
                    │ Role / Skills       │
                    │ Topic               │
                    │ Resume              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Preprocessing Layer │
                    │                     │
                    │ Text Cleaning       │
                    │ Skill Extraction    │
                    │ Project Extraction  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     T5 Generator    │
                    │                     │
                    │ Generate Questions  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    BERT Analyzer    │
                    │                     │
                    │ Similarity          │
                    │ Ranking             │
                    │ Duplicate Removal   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Question Balancing  │
                    │                     │
                    │ Skills              │
                    │ Categories          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Interview Practice  │
                    │                     │
                    │ Answer Evaluation   │
                    │ Score / 100         │
                    │ Missing Concepts    │
                    └─────────────────────┘
```

---

# 🔐 Privacy

Resume processing is performed by the local application when using the provided local pipeline.

Do not upload resumes containing sensitive information to environments you do not trust.

If the application is deployed publicly, review the deployment architecture and privacy requirements before allowing users to upload personal documents.

---

# 🚀 Future Enhancements

Possible improvements include:

* 🎤 Voice-based interview practice
* 🗣️ Speech-to-text answers
* 🔊 Text-to-speech interviewer
* 💬 Conversational AI interviewer
* 📊 Interview performance dashboard
* 🗃️ SQLite score history
* 📈 Progress tracking
* 🧠 Adaptive difficulty
* 🔄 Follow-up questions
* 📄 Improved resume parsing
* 🏆 Interview performance reports
* 🌐 Cloud deployment
* 🔑 API-based LLM support
* 👤 User accounts and personalized history

---

# 💡 Learning Outcomes

This project demonstrates practical knowledge of:

* Transformer architectures
* BERT
* T5
* Hugging Face Transformers
* Tokenization
* NLP preprocessing
* Text similarity
* Semantic ranking
* Text generation
* Resume parsing
* Information extraction
* Streamlit application development
* Model inference
* AI-based evaluation
* Fallback system design

---

# 🎤 Interview Explanation

A concise way to explain the project:

> "I developed an AI-powered interview question generator using Streamlit and Hugging Face Transformers. The system accepts a role, skills, topic, or resume and generates personalized questions. I use FLAN-T5 for question generation and BERT for semantic ranking, duplicate removal, and answer evaluation. I also implemented skill and category balancing and an offline fallback question bank for systems that cannot run the Transformer models."

---

# 📌 Key Technical Point

One of the most important architectural decisions in this project is separating **generation** from **understanding**.

```text
T5
↓
Generates new questions

BERT
↓
Understands semantic meaning
↓
Ranks questions
↓
Detects similar questions
↓
Evaluates candidate answers
```

This demonstrates why different Transformer architectures can be combined rather than using a single model for every NLP task.

---

# 📜 License

This project is intended for educational, portfolio, and interview-preparation purposes.

Add an appropriate open-source license if you plan to distribute the project publicly.

---

# ⭐ Project Highlights

```text
✔ Resume-based question generation
✔ Role and skill-based generation
✔ Topic-based practice
✔ Technical + Coding + Project + HR categories
✔ Beginner / Intermediate / Advanced difficulty
✔ FLAN-T5 question generation
✔ BERT semantic ranking
✔ Near-duplicate removal
✔ Answer scoring
✔ Missing concept detection
✔ Offline question-bank fallback
✔ Streamlit interface
✔ Downloadable question sets
```

---

## 👩‍💻 Author

**Sameeksha Rai**

Artificial Intelligence & Machine Learning | Generative AI | NLP | Deep Learning | Python

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
