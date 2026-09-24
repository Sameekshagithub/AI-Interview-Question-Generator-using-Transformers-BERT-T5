"""
AI Interview Question Generator
Transformers + BERT + Hugging Face + Streamlit (sea green theme)

Run:  streamlit run app.py
"""

import html
import random
import re
from itertools import zip_longest

import streamlit as st

# ----------------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Interview Question Generator",
  
    layout="wide",
)

SEA = "#2E8B57"        # sea green
SEA_DARK = "#1F6B41"
SEA_DEEP = "#123524"
SEA_MID = "#3CB371"
SEA_SOFT = "#D9F0E3"
SEA_MIST = "#F2FAF6"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Manrope', 'Segoe UI', system-ui, sans-serif;
}}
.stApp {{ background: {SEA_MIST}; }}
#MainMenu, footer {{ visibility: hidden; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {SEA_SOFT};
    border-right: 1px solid #b5dfc7;
}}
[data-testid="stSidebar"] .stButton > button {{ width: 100%; }}

/* Hero banner */
.hero {{
    background: linear-gradient(120deg, {SEA_DARK} 0%, {SEA} 55%, {SEA_MID} 100%);
    color: #ffffff;
    padding: 2rem 2.2rem;
    border-radius: 18px;
    margin-bottom: 1.4rem;
}}
.hero h1 {{
    color: #ffffff; margin: 0; font-size: 2.1rem; font-weight: 800;
    letter-spacing: -0.02em;
}}
.hero p {{ margin: .5rem 0 0 0; font-size: 1.02rem; color: #e6f7ee; max-width: 46rem; }}

/* Buttons */
.stButton > button, .stDownloadButton > button {{
    background: {SEA};
    color: #ffffff;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: .55rem 1.2rem;
    transition: background .15s ease;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    background: {SEA_DARK};
    color: #ffffff;
    border: none;
}}
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible {{
    outline: 3px solid {SEA_MID};
    outline-offset: 2px;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 6px; }}
.stTabs [data-baseweb="tab"] {{
    background: {SEA_SOFT}; border-radius: 10px 10px 0 0; padding: .5rem 1.1rem;
    color: {SEA_DEEP}; font-weight: 600;
}}
.stTabs [aria-selected="true"] {{ background: {SEA}; color: #ffffff; }}
.stTabs [data-baseweb="tab-highlight"] {{ background: {SEA_DARK}; }}

/* Question cards */
.qcard {{
    background: #ffffff;
    border: 1px solid #bfe3cf;
    border-left: 6px solid {SEA};
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: .8rem;
}}
.qcard .qtext {{ color: {SEA_DEEP}; font-size: 1.04rem; line-height: 1.55; margin-top: .45rem; }}
.badge {{
    display: inline-block; background: {SEA}; color: #ffffff;
    font-size: .76rem; font-weight: 700; border-radius: 999px;
    padding: .12rem .7rem; margin-right: .35rem;
}}
.badge.soft {{ background: {SEA_SOFT}; color: {SEA_DARK}; }}

/* Metric / result box */
.result {{
    background: #ffffff; border: 1px solid #bfe3cf; border-radius: 12px;
    padding: .9rem 1.1rem; margin-top: .4rem;
}}
.stProgress > div > div > div > div {{ background-color: {SEA}; }}
.small-note {{ color: #3f6b55; font-size: .88rem; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

DIFFS = ["Beginner", "Intermediate", "Advanced"]
CATEGORIES = ["Technical", "Coding", "Project", "HR"]

# ----------------------------------------------------------------------------
# Knowledge base (fallback questions + concepts used to score answers)
# ----------------------------------------------------------------------------
BANK = {
    "python": {
        "Beginner": ["What is the difference between a list and a tuple in Python?",
                     "What are mutable and immutable data types in Python?"],
        "Intermediate": ["Explain decorators and generators in Python with use cases.",
                         "What is the difference between a deep copy and a shallow copy?"],
        "Advanced": ["How does the Global Interpreter Lock affect multithreading, and how would you work around it?",
                     "Explain how Python manages memory and garbage collection."],
    },
    "machine learning": {
        "Beginner": ["What is the difference between supervised and unsupervised learning?",
                     "What is overfitting and how can you detect it?"],
        "Intermediate": ["How would you handle class imbalance in a classification problem?",
                         "Explain the bias-variance trade-off."],
        "Advanced": ["How would you design an ML pipeline for a highly imbalanced streaming dataset?",
                     "How do you monitor a deployed model for data drift and concept drift?"],
    },
    "deep learning": {
        "Beginner": ["What is a neural network and what does an activation function do?",
                     "What is backpropagation?"],
        "Intermediate": ["Explain vanishing and exploding gradients and how to mitigate them.",
                         "What is the role of dropout and batch normalization?"],
        "Advanced": ["Compare Adam, RMSprop and SGD with momentum. When would you prefer each?",
                     "How would you train a very large network with limited GPU memory?"],
    },
    "nlp": {
        "Beginner": ["Explain the purpose of tokenization in NLP.",
                     "How does TF-IDF work?"],
        "Intermediate": ["What are word embeddings, and how do Word2Vec and GloVe differ?",
                         "How would you build a text classification pipeline for customer reviews?"],
        "Advanced": ["How would you handle out-of-vocabulary words and multilingual text in production?",
                     "How do you evaluate a text generation system beyond BLEU?"],
    },
    "bert": {
        "Beginner": ["What does BERT stand for and what problem does it solve?",
                     "How is BERT different from traditional RNNs?"],
        "Intermediate": ["Explain masked language modelling and next sentence prediction in BERT pre-training.",
                         "How would you fine-tune BERT for sentiment analysis?"],
        "Advanced": ["Why is original BERT unsuitable for free-form text generation, and how do encoder-decoder models address this?",
                     "Compare BERT, RoBERTa and DistilBERT in terms of accuracy and efficiency."],
    },
    "transformers": {
        "Beginner": ["What is the self-attention mechanism in Transformers?",
                     "Why did Transformers replace RNNs for many NLP tasks?"],
        "Intermediate": ["Explain multi-head attention and positional encoding.",
                         "What is the difference between encoder-only, decoder-only and encoder-decoder Transformers?"],
        "Advanced": ["How does attention complexity scale with sequence length, and what techniques reduce it?",
                     "Explain parameter-efficient fine-tuning methods such as LoRA."],
    },
    "sql": {
        "Beginner": ["What is the difference between INNER JOIN and LEFT JOIN?",
                     "What is the difference between WHERE and HAVING?"],
        "Intermediate": ["Explain indexing and how it affects query performance.",
                         "What are window functions? Give an example."],
        "Advanced": ["How would you optimise a slow query on a table with millions of rows?",
                     "Explain transaction isolation levels and the problems they prevent."],
    },
    "cnn": {
        "Beginner": ["What is a convolutional layer and why is it useful for images?",
                     "What is pooling and why do we use it?"],
        "Intermediate": ["Why would you choose a CNN for image or emotion recognition instead of a fully connected network?",
                         "How does transfer learning work with pre-trained CNNs?"],
        "Advanced": ["Explain receptive fields and how network depth affects them.",
                     "How would you deal with limited labelled images and class imbalance in a CNN project?"],
    },
    "opencv": {
        "Beginner": ["How does Haar Cascade face detection work?",
                     "How do you read, resize and convert an image to grayscale in OpenCV?"],
        "Intermediate": ["What is the difference between Haar Cascades and DNN-based face detectors?",
                         "How would you process a live webcam stream efficiently with OpenCV?"],
        "Advanced": ["How would you improve face detection under poor lighting and occlusion?",
                     "How would you optimise a real-time OpenCV pipeline for low latency?"],
    },
    "flask": {
        "Beginner": ["What is Flask and how does routing work?",
                     "What is the difference between GET and POST requests?"],
        "Intermediate": ["How would you serve a machine learning model through a Flask API?",
                         "What are Flask blueprints and when would you use them?"],
        "Advanced": ["How would you deploy and scale a Flask model-serving app in production?",
                     "How do you handle concurrency and long-running inference requests in Flask?"],
    },
    "statistics": {
        "Beginner": ["What is the difference between mean, median and mode?",
                     "What is a p-value?"],
        "Intermediate": ["Explain Type I and Type II errors.",
                         "What is the central limit theorem and why does it matter?"],
        "Advanced": ["How would you design and analyse an A/B test with multiple metrics?",
                     "Explain Bayesian versus frequentist inference."],
    },
    "pandas": {
        "Beginner": ["What is the difference between a Series and a DataFrame?",
                     "How do you handle missing values in pandas?"],
        "Intermediate": ["Explain groupby, merge and pivot_table with examples.",
                         "How do loc and iloc differ?"],
        "Advanced": ["How would you process a dataset larger than memory using pandas?",
                     "How can you vectorise operations to avoid slow row-wise apply calls?"],
    },
    "data structures": {
        "Beginner": ["What is the difference between an array and a linked list?",
                     "Explain stacks and queues."],
        "Intermediate": ["How does a hash table handle collisions?",
                         "What is the time complexity of common operations on a binary search tree?"],
        "Advanced": ["How would you design an LRU cache?",
                     "When would you use a heap or a trie? Give real-world examples."],
    },
}

CONCEPTS = {
    "python": ["mutable", "immutable", "list", "tuple", "dictionary", "generator", "decorator", "gil", "memory"],
    "machine learning": ["overfitting", "bias", "variance", "training", "validation", "cross-validation",
                         "regularization", "precision", "recall", "features"],
    "deep learning": ["neural network", "activation", "gradient", "backpropagation", "layer", "dropout", "batch", "loss"],
    "nlp": ["token", "embedding", "tf-idf", "vocabulary", "corpus", "classification", "preprocessing", "lemmatization"],
    "bert": ["bidirectional", "encoder", "transformer", "masked", "pre-train", "fine-tun", "attention", "token"],
    "transformers": ["attention", "self-attention", "encoder", "decoder", "positional", "query", "key", "value", "parallel"],
    "sql": ["join", "index", "group by", "primary key", "null", "aggregate", "query", "table"],
    "cnn": ["convolution", "filter", "kernel", "pooling", "feature map", "stride", "padding", "image"],
    "opencv": ["image", "cascade", "grayscale", "detect", "frame", "haar", "resize", "contour"],
    "flask": ["route", "request", "response", "api", "json", "server", "template", "deploy"],
    "statistics": ["mean", "variance", "distribution", "hypothesis", "sample", "probability", "p-value", "confidence"],
    "pandas": ["dataframe", "series", "groupby", "merge", "missing", "index", "column", "apply"],
    "data structures": ["array", "linked list", "stack", "queue", "tree", "hash", "complexity", "graph"],
}

CODING = {
    "python": ["Write Python code to find duplicate elements in a list.",
               "Write a function to check whether a string is a palindrome.",
               "Write a function that returns the first non-repeating character of a string.",
               "Write a generator that yields the Fibonacci sequence."],
    "sql": ["Write a SQL query to find the second highest salary from an Employee table.",
            "Write a SQL query to find duplicate emails in a Users table.",
            "Write a query to get the top 3 products by revenue in each category."],
    "pandas": ["Using pandas, group sales data by month and compute total revenue.",
               "Write pandas code to fill missing numeric values with the column median."],
    "data structures": ["Implement a stack using two queues.",
                        "Write code to reverse a linked list.",
                        "Write a function to detect a cycle in a linked list."],
    "machine learning": ["Write code to train and evaluate a logistic regression model with scikit-learn.",
                         "Write code to run 5-fold cross-validation and print the mean accuracy."],
    "nlp": ["Write code to clean text and compute TF-IDF vectors with scikit-learn.",
            "Write a function to count word frequencies in a paragraph, ignoring punctuation and case."],
    "deep learning": ["Write a small PyTorch model class for image classification."],
    "cnn": ["Write a Keras or PyTorch CNN with two convolution layers."],
    "opencv": ["Write OpenCV code to detect faces from a webcam feed using a Haar cascade."],
    "flask": ["Write a Flask route that accepts JSON and returns a model prediction."],
    "bert": ["Write code using the Hugging Face pipeline to classify the sentiment of a sentence."],
    "transformers": ["Write code to tokenize a sentence with a Hugging Face tokenizer and print the token IDs."],
}
CODING_GENERAL = ["Write a function to reverse a string without using slicing.",
                  "Write code to find the largest element in a list without using max()."]

HR = [
    "Tell me about yourself.",
    "Why are you interested in this role?",
    "What are your strengths and weaknesses?",
    "Describe a time you worked in a team to solve a difficult problem.",
    "Where do you see yourself in five years?",
    "How do you keep up with new developments in AI and machine learning?",
    "Tell me about a time you failed and what you learned from it.",
    "Why should we hire you?",
    "How do you handle tight deadlines and multiple priorities?",
    "Do you have any questions for us?",
]

ALIASES = {
    "ml": "machine learning", "scikit-learn": "machine learning", "sklearn": "machine learning",
    "dl": "deep learning", "tensorflow": "deep learning", "pytorch": "deep learning", "keras": "deep learning",
    "natural language processing": "nlp", "text mining": "nlp",
    "convolutional neural network": "cnn", "convolutional neural networks": "cnn",
    "cv2": "opencv", "computer vision": "opencv",
    "hugging face": "transformers", "huggingface": "transformers", "transformer": "transformers",
    "dsa": "data structures", "algorithms": "data structures",
    "mysql": "sql", "postgresql": "sql", "sqlite": "sql",
    "streamlit": "python", "numpy": "pandas",
}

TEMPLATES = {
    "Beginner": "What is {s}, and where is it used?",
    "Intermediate": "Describe a practical problem you solved using {s}.",
    "Advanced": "What are the limitations of {s}, and how would you scale or optimise it in production?",
}

SECTION_HEADERS = {
    "education", "skills", "technical skills", "experience", "work experience", "certification",
    "certifications", "achievements", "internship", "internships", "summary", "objective",
    "languages", "interests", "awards", "profile", "declaration",
}


# ----------------------------------------------------------------------------
# Text preprocessing & skill extraction
# ----------------------------------------------------------------------------
def clean_text(text: str) -> str:
    text = re.sub(r"[^\w\s,.;:+#/&()\-]", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def _find(term: str, text: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None


def extract_skills(text: str) -> list:
    """Find known skills (and their aliases) inside free text."""
    text = (text or "").lower()
    hits = []
    for term in list(BANK.keys()) + list(ALIASES.keys()):
        if _find(term, text):
            canon = ALIASES.get(term, term)
            if canon not in hits:
                hits.append(canon)
    return hits


def parse_skill_list(raw: str) -> list:
    """Comma separated skills -> canonical skills (unknown ones are kept as custom)."""
    skills = []
    for item in re.split(r"[,;\n]", raw or ""):
        item = item.strip().lower()
        if not item:
            continue
        found = extract_skills(item)
        canon = found[0] if found else item
        if canon not in skills:
            skills.append(canon)
    return skills


def read_pdf(uploaded_file) -> str:
    import fitz  # PyMuPDF

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def extract_projects(resume_text: str) -> list:
    """Very simple project-title detector based on a 'Projects' section."""
    lines = [l.strip() for l in (resume_text or "").splitlines()]
    start = None
    for i, l in enumerate(lines):
        if re.fullmatch(r"(academic |personal |major |key )?projects?", l.lower().strip(": ")):
            start = i + 1
            break
    if start is None:
        return []
    projects = []
    for l in lines[start:]:
        low = l.lower().strip(": ")
        if low in SECTION_HEADERS:
            break
        if not l or l[0] in "•-*▪●◦":
            continue
        if l.count(",") >= 2 or l.endswith(".") or not 4 <= len(l) <= 90:
            continue
        title = re.sub(r"\s*[|(].*$|\s+[–—-]\s+.*$", "", l).strip()
        if title and title not in projects:
            projects.append(title)
        if len(projects) >= 5:
            break
    return projects


# ----------------------------------------------------------------------------
# Hugging Face models (BERT encoder + T5 generator)
# ----------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading BERT encoder from Hugging Face...")
def load_bert(name: str = "bert-base-uncased"):
    from transformers import AutoModel, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModel.from_pretrained(name)
    model.eval()
    return tok, model


@st.cache_resource(show_spinner="Loading generative Transformer (T5) from Hugging Face...")
def load_t5(name: str):
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForSeq2SeqLM.from_pretrained(name)
    model.eval()
    return tok, model


def embed(texts, bert):
    """BERT tokenization -> encoder -> mean pooling -> L2-normalised vectors."""
    import torch

    tok, model = bert
    enc = tok(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
    with torch.no_grad():
        hidden = model(**enc).last_hidden_state
    mask = enc["attention_mask"].unsqueeze(-1).float()
    vec = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
    return torch.nn.functional.normalize(vec, dim=1)


def t5_questions(skill, role, level, exp, t5, bert=None, keep=3):
    """Generate candidate questions with T5, then rank them with BERT."""
    import torch

    tok, model = t5
    prompt = (f"Write one {level.lower()} technical interview question about {skill} "
              f"for a {exp.lower()} {role}.")
    try:
        enc = tok(prompt, return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            out = model.generate(
                **enc, max_new_tokens=48, do_sample=True, top_p=0.92,
                temperature=0.95, num_return_sequences=6,
            )
        cands = []
        for o in out:
            q = re.sub(r"\s+", " ", tok.decode(o, skip_special_tokens=True)).strip()
            if q.endswith("?") and 20 <= len(q) <= 220 and q.lower() not in [c.lower() for c in cands]:
                cands.append(q)
        if bert and len(cands) > 1:
            vecs = embed(cands + [f"interview question about {skill}"], bert)
            scores = (vecs[:-1] @ vecs[-1]).tolist()
            cands = [c for _, c in sorted(zip(scores, cands), reverse=True)]
        return cands[:keep]
    except Exception:
        return []


def dedupe(items, bert=None, threshold=0.95):
    seen, uniq = set(), []
    for it in items:
        key = re.sub(r"\W+", " ", it["q"].lower()).strip()
        if key not in seen:
            seen.add(key)
            uniq.append(it)
    if bert and len(uniq) > 1:
        vecs = embed([i["q"] for i in uniq], bert)
        keep = []
        for i in range(len(uniq)):
            if all(float(vecs[i] @ vecs[j]) < threshold for j in keep):
                keep.append(i)
        uniq = [uniq[i] for i in keep]
    return uniq


# ----------------------------------------------------------------------------
# Question builder
# ----------------------------------------------------------------------------
def allocate(n, cats):
    base, extra = divmod(n, len(cats))
    return {c: base + (1 if i < extra else 0) for i, c in enumerate(cats)}


def round_robin(pools, k):
    pools = {s: list(p) for s, p in pools.items()}
    out = []
    while len(out) < k and any(pools.values()):
        for s in list(pools):
            if pools[s] and len(out) < k:
                out.append((s, pools[s].pop(0)))
    return out


def technical_pool(skill, level, ai_cands):
    bank = BANK.get(skill, {})
    primary = [(q, level) for q in bank.get(level, [])]
    if skill not in BANK:
        primary = [(TEMPLATES[level].format(s=skill), level)]
    random.shuffle(primary)
    ai = [(q, level) for q in ai_cands]
    merged = [x for pair in zip_longest(primary, ai) for x in pair if x]
    others = [(q, l) for l in DIFFS if l != level for q in bank.get(l, [])]
    random.shuffle(others)
    return merged + others


def build_questions(role, skills, level, exp, total, cats, projects, t5=None, bert=None):
    random.seed()
    skills = skills or ["python", "machine learning"]
    alloc = allocate(total, cats)
    items = []

    # Technical
    if "Technical" in cats:
        k = alloc["Technical"]
        pools = {}
        for s in skills[:8]:
            ai = t5_questions(s, role, level, exp, t5, bert) if t5 else []
            pools[s] = technical_pool(s, level, ai)
        picked = round_robin(pools, k * 2)
        cand = [{"q": q, "category": "Technical", "skill": s, "difficulty": lv} for s, (q, lv) in picked]
        items += dedupe(cand, bert)[:k]

    # Coding
    if "Coding" in cats:
        k = alloc["Coding"]
        pools = {}
        for s in skills:
            if s in CODING:
                pool = list(CODING[s])
                random.shuffle(pool)
                pools[s] = pool
        pools["general"] = random.sample(CODING_GENERAL, len(CODING_GENERAL))
        picked = round_robin(pools, k)
        items += [{"q": q, "category": "Coding", "skill": s, "difficulty": level} for s, q in picked]

    # Project
    if "Project" in cats:
        k = alloc["Project"]
        cand = []
        for p in projects:
            cand += [
                f"Explain the architecture of your {p} project.",
                f"What challenges did you face while building {p}, and how did you solve them?",
                f"How did you evaluate or test {p}? Which metrics did you use?",
            ]
        for s in skills:
            cand.append(f"Why did you choose {s.upper() if len(s) <= 4 else s.title()} in your project, and what alternatives did you consider?")
        cand += [
            "Explain how you implemented your most recent machine learning project.",
            "What was the most difficult bug or failure in your project and how did you fix it?",
            "If you had more time, how would you improve your project?",
        ]
        items += [{"q": q, "category": "Project", "skill": "project", "difficulty": level} for q in cand[:k]]

    # HR
    if "HR" in cats:
        k = alloc["HR"]
        hr = random.sample(HR, min(k, len(HR)))
        items += [{"q": q, "category": "HR", "skill": "general", "difficulty": level} for q in hr]

    order = {c: i for i, c in enumerate(CATEGORIES)}
    items.sort(key=lambda x: order[x["category"]])
    return items


# ----------------------------------------------------------------------------
# Answer evaluation (BERT similarity + concept coverage)
# ----------------------------------------------------------------------------
def evaluate_answer(answer, item, bert=None):
    answer = (answer or "").strip()
    if not answer:
        return None
    low = answer.lower()
    concepts = CONCEPTS.get(item["skill"], [])
    matched = [c for c in concepts if c in low]
    missing = [c for c in concepts if c not in low]
    coverage = len(matched) / len(concepts) if concepts else None
    length_f = min(len(answer.split()) / 30, 1.0)

    sim = None
    if bert:
        ref = item["q"] + " " + " ".join(concepts)
        v = embed([answer, ref], bert)
        raw = float(v[0] @ v[1])
        sim = max(0.0, min((raw - 0.6) / 0.3, 1.0))   # rough calibration for raw BERT cosine

    parts = []
    if coverage is not None:
        parts.append((0.5 if sim is not None else 0.75, coverage))
    if sim is not None:
        parts.append((0.3 if coverage is not None else 0.6, sim))
    parts.append((0.2 if (coverage is not None and sim is not None) else 0.25 if coverage is not None
                  else 0.4 if sim is not None else 1.0, length_f))
    total_w = sum(w for w, _ in parts)
    score = 100 * sum(w * v for w, v in parts) / total_w
    return {"score": round(score), "matched": matched, "missing": missing[:6], "sim": sim, "words": len(answer.split())}


# ----------------------------------------------------------------------------
# UI helpers
# ----------------------------------------------------------------------------
def render_cards(items):
    for i, it in enumerate(items, 1):
        st.markdown(
            f'<div class="qcard">'
            f'<span class="badge">{html.escape(it["category"])}</span>'
            f'<span class="badge soft">{html.escape(it["difficulty"])}</span>'
            f'<span class="badge soft">{html.escape(it["skill"].title())}</span>'
            f'<div class="qtext"><b>Q{i}.</b> {html.escape(it["q"])}</div></div>',
            unsafe_allow_html=True,
        )


def items_to_text(items, role):
    lines = [f"Interview questions for: {role}", ""]
    for i, it in enumerate(items, 1):
        lines.append(f"Q{i}. [{it['category']} | {it['difficulty']} | {it['skill'].title()}] {it['q']}")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
st.session_state.setdefault("items", [])
st.session_state.setdefault("meta", {})
st.session_state.setdefault("results", {})

with st.sidebar:
    st.markdown("### 🌊 Interview setup")
    mode = st.radio("Input type", ["Role and skills", "Topic", "Resume (PDF or text)"])

    role = st.text_input("Job role", "AI Engineer")
    exp = st.selectbox("Experience", ["Fresher", "Junior", "Mid-level", "Senior"])

    skills_raw, topic_raw, resume_text = "", "", ""
    if mode == "Role and skills":
        skills_raw = st.text_input("Skills (comma separated)", "Python, Machine Learning, NLP, BERT")
    elif mode == "Topic":
        topic_raw = st.text_input("Topic", "Transformers")
    else:
        pdf = st.file_uploader("Upload resume (PDF)", type=["pdf"])
        pasted = st.text_area("...or paste resume text", height=120)
        if pdf is not None:
            try:
                resume_text = read_pdf(pdf)
            except Exception as e:
                st.error(f"Could not read the PDF: {e}")
        if not resume_text:
            resume_text = pasted

    level = st.select_slider("Difficulty", options=DIFFS, value="Intermediate")
    total = st.slider("Number of questions", 3, 20, 8)
    cats = st.multiselect("Question categories", CATEGORIES, default=["Technical", "Coding", "Project", "HR"])

    st.markdown("---")
    use_ai = st.toggle("Use Hugging Face AI models", value=True,
                       help="Loads BERT (ranking, de-duplication, answer scoring) and T5 (question generation). "
                            "The first run downloads the models. Turn off for instant question-bank mode.")
    t5_name = st.selectbox("Generative model", ["google/flan-t5-small", "google/flan-t5-base"], index=0,
                           disabled=not use_ai,
                           help="flan-t5-small is fast. flan-t5-base gives better questions but is ~1 GB.")
    go = st.button("Generate questions")

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="hero"><h1>AI Interview Question Generator</h1>'
    "<p>Enter a role, a topic or your resume and get tailored technical, coding, project and HR questions. "
    "Then answer them and get scored feedback.</p></div>",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Generate
# ----------------------------------------------------------------------------
if go:
    if not cats:
        st.warning("Select at least one question category.")
    else:
        raw = clean_text(resume_text) if mode.startswith("Resume") else ""
        if mode == "Role and skills":
            skills = parse_skill_list(skills_raw)
        elif mode == "Topic":
            skills = parse_skill_list(topic_raw)
        else:
            skills = extract_skills(raw)
        projects = extract_projects(resume_text) if mode.startswith("Resume") else []

        if mode.startswith("Resume") and not raw:
            st.warning("Upload a resume PDF or paste resume text first.")
        else:
            bert = t5 = None
            if use_ai:
                try:
                    bert = load_bert()
                    t5 = load_t5(t5_name)
                except Exception as e:
                    st.warning(f"Could not load the Hugging Face models ({e}). Using the built-in question bank instead.")
                    bert = t5 = None
            with st.spinner("Generating questions..."):
                st.session_state["items"] = build_questions(
                    role or "AI Engineer", skills, level, exp, total, cats, projects, t5, bert)
            st.session_state["meta"] = {"role": role, "skills": skills, "projects": projects,
                                        "ai": bool(bert and t5)}
            st.session_state["results"] = {}

# ----------------------------------------------------------------------------
# Tabs
# ----------------------------------------------------------------------------
tab_gen, tab_practice, tab_about = st.tabs(["Questions", "Practice and feedback", "How it works"])

with tab_gen:
    items = st.session_state["items"]
    meta = st.session_state["meta"]
    if not items:
        st.info("Fill in the sidebar and select **Generate questions** to begin.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Questions", len(items))
        c2.metric("Skills detected", len(meta.get("skills", [])) or "default")
        c3.metric("Engine", "BERT + T5" if meta.get("ai") else "Question bank")
        if meta.get("skills"):
            st.markdown("**Skills used:** " + ", ".join(s.title() for s in meta["skills"]))
        if meta.get("projects"):
            st.markdown("**Projects found in resume:** " + ", ".join(meta["projects"]))
        st.write("")
        render_cards(items)
        st.download_button("Download questions (.txt)", items_to_text(items, meta.get("role", "")),
                           file_name="interview_questions.txt")

with tab_practice:
    items = st.session_state["items"]
    if not items:
        st.info("Generate questions first, then write your answers here.")
    else:
        st.markdown('<p class="small-note">Write an answer for each question you want feedback on. '
                    "Scoring combines key-concept coverage, answer length and (when AI models are on) "
                    "BERT semantic similarity. Treat it as a practice guide, not a verdict.</p>",
                    unsafe_allow_html=True)
        for i, it in enumerate(items):
            with st.expander(f"Q{i + 1}. {it['q']}"):
                st.text_area("Your answer", key=f"ans_{i}", height=110)
                res = st.session_state["results"].get(i)
                if res:
                    st.progress(res["score"] / 100)
                    st.markdown(
                        f'<div class="result"><b>Score: {res["score"]}/100</b> &nbsp; ({res["words"]} words)<br>'
                        f'{"<b>Covered:</b> " + ", ".join(res["matched"]) + "<br>" if res["matched"] else ""}'
                        f'{"<b>Consider mentioning:</b> " + ", ".join(res["missing"]) if res["missing"] else ""}'
                        f"</div>", unsafe_allow_html=True)

        if st.button("Evaluate my answers"):
            bert = None
            if st.session_state["meta"].get("ai"):
                try:
                    bert = load_bert()
                except Exception:
                    bert = None
            results = {}
            for i, it in enumerate(items):
                r = evaluate_answer(st.session_state.get(f"ans_{i}", ""), it, bert)
                if r:
                    results[i] = r
            st.session_state["results"] = results
            st.rerun()

        results = st.session_state["results"]
        if results:
            avg = sum(r["score"] for r in results.values()) / len(results)
            st.markdown("---")
            m1, m2 = st.columns(2)
            m1.metric("Answers evaluated", f"{len(results)} / {len(items)}")
            m2.metric("Average score", f"{avg:.0f} / 100")
            if avg >= 75:
                st.success("Strong answers. Keep practising harder questions.")
            elif avg >= 50:
                st.info("Good base. Add more of the key concepts listed under each question.")
            else:
                st.warning("Review the fundamentals for the topics above and try again with longer, more specific answers.")

with tab_about:
    st.markdown(
        """
**Pipeline**

1. **Input** – role, skills, topic, or a resume PDF (text extracted with PyMuPDF).
2. **Preprocessing** – clean text, extract skills and project titles, build prompts.
3. **Tokenization** – Hugging Face tokenizers turn text into token IDs.
4. **BERT (encoder)** – produces embeddings used to rank generated questions, remove near-duplicates and
   compare your answers with the expected concepts.
5. **T5 (generative Transformer)** – writes new technical questions from prompts. Original BERT is an
   encoder-only model and cannot generate free-form text on its own.
6. **Post-processing** – keep well-formed questions, balance across skills and categories.
7. **Streamlit UI** – questions, download, and practice feedback.

**Interview tip:** the models are pre-trained Hugging Face checkpoints used for inference. Nothing is trained from scratch.
        """
    )
