<p align="center">
  <h1 align="center">Exoplanet Explorer AI</h1>
  <p align="center">
    <strong>A multilingual, voice-enabled RAG chatbot that makes exoplanet discoveries accessible and captivating.</strong>
  </p>
  <p align="center">
    Built with FastAPI · LangChain · Groq (Llama 3.3 70B) · ChromaDB · NASA Exoplanet Archive
  </p>
</p>

---

## About The Project

Exoplanet Explorer AI is a **Retrieval-Augmented Generation (RAG)** chatbot that lets you explore the cosmos through conversation. It pulls real scientific data from **NASA's Exoplanet Archive** — covering 6,300+ confirmed exoplanets — and uses an LLM to transform raw astronomical data into engaging, accurate, and wonder-filled answers.

Ask it about TRAPPIST-1, hot Jupiters, or the latest JWST discoveries. Speak your question in Spanish. Hit the dice button and discover a random alien world you've never heard of. Every answer comes with a fun fact.

### Why This Exists

Exoplanet data is publicly available but buried in dense CSV tables full of technical columns like `pl_bmasse` and `st_teff`. This project bridges that gap — it retrieves the raw data, then uses an LLM persona to explain it the way an enthusiastic astronomer friend would, not a textbook.

---

## Key Features

| Feature | Description |
|---|---|
| **RAG-Powered Answers** | Retrieves relevant exoplanet data from a ChromaDB vector store before generating answers — grounded in real NASA data, not hallucinations |
| **Multi-Language Support** | Chat in English, Spanish, French, German, Japanese, or Hindi — the bot responds in your chosen language |
| **Voice Input & Output** | Speak your questions using the browser's Web Speech API and hear responses read aloud in your selected language |
| **Random Planet Discovery** | Click the dice button to get a random exoplanet from the full 6,300+ dataset with an enthusiastic deep-dive |
| **Conversation Memory** | Remembers your last 5 exchanges so you can ask natural follow-ups like "How far is it?" or "What about its star?" |
| **Space-Themed UI** | Glassmorphism design with animated starfield background, gradient accents, and smooth micro-animations |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Browser (Frontend)                │
│  ┌───────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Speech-to │  │  Chat UI │  │  Text-to-Speech  │  │
│  │   Text    │  │ (JS/CSS) │  │   (Web Speech)   │  │
│  └─────┬─────┘  └────┬─────┘  └────────▲─────────┘  │
│        │             │                  │            │
└────────┼─────────────┼──────────────────┼────────────┘
         │             │                  │
         ▼             ▼                  │
┌─────────────────────────────────────────┼────────────┐
│              FastAPI Backend            │            │
│  ┌──────────────────────────────────────┼──────────┐ │
│  │            RAG Engine                │          │ │
│  │  ┌──────────┐  ┌──────────────┐  ┌──┴───────┐  │ │
│  │  │ ChromaDB │  │  LangChain   │  │  Groq    │  │ │
│  │  │ (Vector  │◄─┤  Retrieval   │─►│  LLM     │  │ │
│  │  │  Store)  │  │  + Prompt    │  │ (Llama   │  │ │
│  │  └──────────┘  └──────────────┘  │  3.3 70B)│  │ │
│  │                                  └──────────┘  │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
         ▲
         │ (Build Step)
┌────────┴────────────────┐
│  NASA Exoplanet Archive │
│  (TAP API → CSV → DB)  │
└─────────────────────────┘
```

### How It Works

1. **Data Ingestion** — `download_data.py` fetches the latest confirmed exoplanet data from NASA's Table Access Protocol (TAP) API and saves it as a CSV.
2. **Embedding & Indexing** — On first startup, `rag_engine.py` reads the CSV, formats each planet's data into a descriptive text chunk, embeds them using `fastembed` (an extremely lightweight ONNX-based embedding engine that avoids PyTorch RAM bloat), and stores them in a ChromaDB vector database.
3. **Query Flow** — When you ask a question, the retriever finds the 5 most relevant exoplanet entries, injects them as context into a carefully crafted system prompt, and sends everything to the Groq-hosted Llama 3.3 70B model.
4. **Memory** — The last 5 conversation pairs are maintained in-memory and passed to the LLM so follow-up questions work naturally.
5. **Random Planet** — When triggered, the system bypasses vector search entirely, picks a random row from the full CSV, and asks the LLM to present it enthusiastically.

---

## Project Structure

```
rag_chatbot/
├── public/                  # Frontend static files
│   ├── index.html           # Chat interface structure
│   ├── style.css            # Space-themed glassmorphism styling
│   └── script.js            # Web Speech API, chat logic, DOM updates
├── data/
│   └── exoplanets.csv       # NASA dataset (auto-downloaded)
├── chroma_db/               # ChromaDB vector store (auto-generated)
├── main.py                  # FastAPI server & API routes
├── rag_engine.py            # LangChain RAG pipeline, persona, memory
├── download_data.py         # NASA Exoplanet Archive data fetcher
├── requirements.txt         # Python dependencies
├── render.yaml              # Render deployment blueprint
├── .env                     # API keys (not committed)
├── .gitignore               # Git ignore rules
└── README.md                # You are here
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com) (for the LLM)
- A modern browser (Chrome/Edge recommended for voice features)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/sharmapragalbh565-lgtm/exoplaner-explorer.git
cd exoplaner-explorer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the NASA exoplanet dataset
python download_data.py

# 4. Create your .env file with your Groq API key
echo GROQ_API_KEY=gsk_your_key_here > .env

# 5. Start the server
python -m uvicorn main:app --reload
```

Open **http://localhost:8000** in your browser.

> **Note:** The first query will take ~30-60 seconds as ChromaDB embeds and indexes the exoplanet dataset locally. Subsequent queries are near-instant.

---

## Usage Examples

| You Say | What Happens |
|---|---|
| *"Tell me about TRAPPIST-1 e"* | Retrieves data for TRAPPIST-1 e from the vector store, explains its habitability potential with a fun fact |
| *"What about its star?"* | Uses conversation memory to understand "its" refers to TRAPPIST-1, explains the host star |
| *(click dice button)* | Picks a random planet from 6,300+ entries and gives you an enthusiastic breakdown |
| *(click mic, speak in Spanish)* | Transcribes your speech, sends it to the LLM, responds in Spanish text + audio |
| *"Why are there so many hot Jupiters?"* | Uses its knowledge to explain detection bias and planetary migration |

---

## Supported Languages

| Language | Code | Voice Support |
|---|---|---|
| English (US) | `en-US` | Yes — Input + Output |
| Español | `es-ES` | Yes — Input + Output |
| Français | `fr-FR` | Yes — Input + Output |
| Deutsch | `de-DE` | Yes — Input + Output |
| Japanese | `ja-JP` | Yes — Input + Output |
| Hindi | `hi-IN` | Yes — Input + Output |

> Voice features use the browser's native Web Speech API. Best support in Chrome and Edge.

---

## Data Source

This project uses the **NASA Exoplanet Archive**, maintained by the NASA Exoplanet Science Institute (NExScI) at Caltech/IPAC.

- **Archive**: [exoplanetarchive.ipac.caltech.edu](https://exoplanetarchive.ipac.caltech.edu/)
- **Table**: Planetary Systems (`ps`) with `default_flag=1`
- **Fields Used**: Planet name, host star, discovery method, discovery year, mass (Earth masses), radius (Earth radii), orbital period, equilibrium temperature, star temperature, star mass, system distance

The dataset is fetched dynamically via the TAP (Table Access Protocol) API, so running `download_data.py` always gives you the latest confirmed exoplanet data.

---

## Running with Docker

Docker is the easiest way to run this project without installing Python or managing dependencies manually.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- Your Groq API key in the `.env` file

### Quick Start

```bash
# Build and start the container (downloads NASA data automatically)
docker compose up --build

# To run in the background
docker compose up --build -d

# Stop the container
docker compose down
```

Open **http://localhost:8000** in your browser.

The ChromaDB vector store is persisted in a Docker volume (`chroma_data`) so embeddings are preserved across container restarts — you won't have to re-embed the dataset every time you restart.

### Individual Docker Commands

```bash
# Build the image manually
docker build -t exoplanet-chatbot .

# Run the container, passing your API key
docker run -p 8000:8000 -e GROQ_API_KEY=gsk_your_key_here exoplanet-chatbot
```

---

## Deployment (Render)

This project includes a [`render.yaml`](render.yaml) blueprint for one-click deployment.

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New** → **Blueprint**
3. Connect your repo — Render auto-detects `render.yaml`
4. Add your `GROQ_API_KEY` in the Environment tab
5. Deploy

Your app will be live at `https://exoplanet-explorer.onrender.com` (or your custom name).

---

## Tech Stack

| Component | Technology | Why |
|---|---|---|
| **Backend** | FastAPI | Async, fast, auto-docs at `/docs` |
| **LLM** | Groq (Llama 3.3 70B) | Fastest inference available (~300 tok/s), generous free tier |
| **Embeddings** | `fastembed` | Extremely lightweight (<150MB RAM), uses ONNX instead of PyTorch, fits perfectly in free tier hostings like Render |
| **Vector DB** | ChromaDB | Lightweight, file-based, no external server needed |
| **Orchestration** | LangChain (LCEL) | Clean prompt chaining with memory management |
| **Data Source** | NASA Exoplanet Archive | Authoritative, real-time, free access via TAP API |
| **Frontend** | Vanilla HTML/CSS/JS | Zero build step, instant load, full Web Speech API control |
| **Voice** | Web Speech API | Native browser support, no external service needed |

---

## License

This project is open source and available under the [MIT License](LICENSE).
