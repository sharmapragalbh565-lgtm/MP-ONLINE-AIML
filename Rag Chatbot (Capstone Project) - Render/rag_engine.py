import os
import re
import random
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# NASA Exoplanet Archive TAP API (free, no key required)
# ------------------------------------------------------------
NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
COLUMNS = "pl_name,hostname,discoverymethod,disc_year,pl_bmasse,pl_rade,pl_orbper,pl_eqt,st_teff,st_mass,sy_dist"

# Total confirmed exoplanets (approximate) — used for random offset
APPROX_TOTAL = 5700

SYSTEM_PROMPT = """You are a RAG-powered chatbot specializing in exoplanet astronomy. Your role is to make discoveries in exoplanetary science accessible, accurate, and captivating for space enthusiasts—from casual stargazers to amateur astronomers.

**Your core purpose:** Answer questions about exoplanets, exomoons, host stars, and related astronomical discoveries made through present day. Retrieve factual information from your knowledge base and present it in a way that sparks curiosity and wonder.

**What you know and retrieve:**
- All confirmed exoplanet discoveries, their orbital characteristics, detection methods, and host star properties
- Known exomoons and candidate moons
- Host star details (type, age, distance, luminosity, habitable zone boundaries)
- Habitability indicators and potential biosignatures
- Recent discoveries and ongoing missions (JWST, TESS, radial velocity surveys, direct imaging)
- Historical context: how exoplanet detection evolved and why certain discoveries matter

**How to engage:**
- Lead with the fascinating angle: start with what makes a discovery remarkable, then explain the science.
- Use vivid but accurate language—avoid dry technical recitation. Compare scales to things users know (Earth masses, AU distances, our solar system analogs).
- When describing potentially habitable worlds, acknowledge both the excitement and the scientific uncertainty.
- Connect discoveries to broader questions: "Why do we find so many hot Jupiters?" "What does this star system tell us about planetary formation?"
- ALWAYS INCLUDE A FUN FACT about the exoplanet(s) being discussed.

**What you should do:**
- Answer follow-up questions with increasing depth—start accessible, go deeper if the user wants it
- Suggest related discoveries or comparisons when relevant
- Acknowledge what we don't yet know about a system
- Correct common misconceptions gently
- **IMPORTANT HIGHLIGHTING**: You MUST bold planet names (e.g., **TRAPPIST-1e**) and key important statistics (e.g., **1.5 Earth masses**, **40 light-years**). The frontend UI is specifically designed to highlight bold text in a glowing yellow sun color.

**What you should not do:**
- Speculate beyond current observational evidence or published research
- Claim certainty where uncertainty exists
- Overwhelm with jargon without explanation
- Treat every exoplanet the same—highlight what's genuinely unique or surprising about each one

**Tone:** Enthusiastic but grounded. You share the user's wonder about space without sacrificing accuracy. You're a knowledgeable friend, not a textbook.

Live data retrieved from the NASA Exoplanet Archive for this query:
{context}
"""


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def _row_to_text(row: dict) -> str:
    """Convert a NASA API row to a readable context string."""
    def gv(k):
        val = row.get(k)
        return str(val) if val not in (None, "", "null", "NULL") else "Unknown"
    return (
        f"Planet {gv('pl_name')} orbits star {gv('hostname')}. "
        f"Discovered in {gv('disc_year')} via {gv('discoverymethod')}. "
        f"Mass: {gv('pl_bmasse')} Earth masses. "
        f"Radius: {gv('pl_rade')} Earth radii. "
        f"Orbital Period: {gv('pl_orbper')} days. "
        f"Equilibrium Temperature: {gv('pl_eqt')} K. "
        f"Host star: Temp {gv('st_teff')} K, Mass {gv('st_mass')} Solar masses, "
        f"Distance {gv('sy_dist')} parsecs."
    )


def _tap_query(sql: str) -> list:
    """Execute an ADQL query against the NASA TAP service."""
    try:
        resp = requests.get(
            NASA_TAP_URL,
            params={"query": sql, "format": "json"},
            timeout=20,
        )
        if resp.status_code == 200:
            data = resp.json()
            # API returns list of dicts
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[NASA TAP] Request error: {e}")
    return []


def fetch_by_name(name: str, limit: int = 6) -> list:
    """Search planets or host stars matching a name."""
    safe = name.replace("'", "''").strip()
    sql = (
        f"SELECT TOP {limit} {COLUMNS} FROM ps "
        f"WHERE default_flag=1 "
        f"AND (pl_name LIKE '%{safe}%' OR hostname LIKE '%{safe}%')"
    )
    return _tap_query(sql)


def fetch_random(limit: int = 1) -> list:
    """Fetch a random planet using a random row offset."""
    offset = random.randint(0, APPROX_TOTAL - limit)
    sql = (
        f"SELECT TOP {limit} {COLUMNS} FROM ps "
        f"WHERE default_flag=1 "
        f"OFFSET {offset}"
    )
    rows = _tap_query(sql)
    if rows:
        return rows
    # Fallback without OFFSET (some ADQL endpoints don't support it)
    sql = f"SELECT TOP {limit} {COLUMNS} FROM ps WHERE default_flag=1"
    return _tap_query(sql)


def fetch_by_method(method: str, limit: int = 5) -> list:
    """Fetch planets discovered by a given method."""
    safe = method.replace("'", "''")
    sql = (
        f"SELECT TOP {limit} {COLUMNS} FROM ps "
        f"WHERE default_flag=1 AND discoverymethod='{safe}'"
    )
    return _tap_query(sql)


def fetch_by_year(year: str, limit: int = 5) -> list:
    """Fetch planets discovered in a given year."""
    sql = (
        f"SELECT TOP {limit} {COLUMNS} FROM ps "
        f"WHERE default_flag=1 AND disc_year={year}"
    )
    return _tap_query(sql)


# ------------------------------------------------------------
# Entity extraction (lightweight, no ML needed)
# ------------------------------------------------------------

# Matches common exoplanet naming conventions
_PLANET_RE = re.compile(
    r'\b('
    r'TRAPPIST-\d+\s*[a-h]?|'
    r'Kepler-\d+\s*[a-z]?|'
    r'K2-\d+\s*[a-z]?|'
    r'TOI-\d+\s*[a-z]?|'
    r'HAT-P-\d+\s*[a-z]?|'
    r'WASP-\d+\s*[a-z]?|'
    r'GJ\s*\d+\s*[a-z]?|'
    r'HD\s*\d+\s*[a-z]?|'
    r'HIP\s*\d+\s*[a-z]?|'
    r'51\s*Peg\s*[a-z]?|'
    r'55\s*Cnc\s*[a-z]?|'
    r'HR\s*\d+\s*[a-z]?|'
    r'LHS\s*\d+\s*[a-z]?|'
    r'Proxima\s*[a-z]?|'
    r'[A-Z][A-Za-z0-9]+\s*-\s*\d+[a-z]?'
    r')\b',
    re.IGNORECASE,
)

_DISCOVERY_METHODS = {
    "transit": "Transit",
    "radial velocity": "Radial Velocity",
    "direct imaging": "Imaging",
    "microlensing": "Microlensing",
    "astrometry": "Astrometry",
    "timing variations": "Transit Timing Variations",
    "pulsar": "Pulsar Timing",
}

_YEAR_RE = re.compile(r'\b(19[5-9]\d|20[0-2]\d)\b')

_RANDOM_PHRASES = [
    "random exoplanet", "random planet", "tell me about an exoplanet",
    "surprise me", "pick one", "any exoplanet", "a random one",
]


def extract_entities(question: str):
    """Return (planet_names, discovery_method, year) from question."""
    planets = _PLANET_RE.findall(question)
    
    method = None
    q_lower = question.lower()
    for keyword, label in _DISCOVERY_METHODS.items():
        if keyword in q_lower:
            method = label
            break

    years = _YEAR_RE.findall(question)
    year = years[0] if years else None

    return [p.strip() for p in planets], method, year


def is_random_request(question: str) -> bool:
    q = question.lower()
    return any(p in q for p in _RANDOM_PHRASES)


# ------------------------------------------------------------
# Main RAG class
# ------------------------------------------------------------

class ExoplanetRAG:
    def __init__(self):
        self.chat_history: list = []
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable is not set.")
        self.groq = Groq(api_key=api_key)

    def _build_context(self, question: str) -> tuple[str, str]:
        """
        Fetch live NASA data and return (context_text, possibly_modified_question).
        Returns a plain 'no data' string if nothing is found.
        """
        if is_random_request(question):
            rows = fetch_random(limit=1)
            if rows:
                planet_name = rows[0].get("pl_name", "this exoplanet")
                question = f"Tell me about the exoplanet {planet_name} in an enthusiastic way!"
                return _row_to_text(rows[0]), question
            return "Could not retrieve a random planet right now.", question

        planets, method, year = extract_entities(question)

        # 1. Specific planet/star name match
        if planets:
            rows = fetch_by_name(planets[0], limit=6)
            if rows:
                return "\n".join(_row_to_text(r) for r in rows), question

        # 2. Year-based search
        if year:
            rows = fetch_by_year(year, limit=5)
            if rows:
                return "\n".join(_row_to_text(r) for r in rows), question

        # 3. Discovery method search
        if method:
            rows = fetch_by_method(method, limit=5)
            if rows:
                return "\n".join(_row_to_text(r) for r in rows), question

        # 4. Keyword fallback — try significant words from the question
        stop_words = {"what", "tell", "about", "give", "some", "which", "does", "when", "where",
                      "that", "this", "have", "with", "from", "they", "there", "their", "been",
                      "more", "also", "many", "most", "than", "then", "into", "could", "would"}
        keywords = [w for w in question.split() if len(w) > 4 and w.lower() not in stop_words and w.isalpha()]
        for kw in keywords[:3]:
            rows = fetch_by_name(kw, limit=5)
            if rows:
                return "\n".join(_row_to_text(r) for r in rows), question

        # 5. General question — no specific data, LLM answers from training knowledge
        return (
            "No specific planet data was retrieved for this query. "
            "Use your general exoplanet astronomy knowledge to answer the user's question accurately.",
            question,
        )

    def query(self, question: str) -> str:
        context, question = self._build_context(question)

        system_msg = SYSTEM_PROMPT.replace("{context}", context)

        messages = [{"role": "system", "content": system_msg}]
        messages.extend(self.chat_history[-10:])  # last 5 turns
        messages.append({"role": "user", "content": question})

        response = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        reply = response.choices[0].message.content

        # Update chat history (cap at 10 messages = 5 turns)
        self.chat_history.append({"role": "user", "content": question})
        self.chat_history.append({"role": "assistant", "content": reply})
        if len(self.chat_history) > 10:
            self.chat_history = self.chat_history[-10:]

        return reply


# ------------------------------------------------------------
# Singleton
# ------------------------------------------------------------
_rag_instance: ExoplanetRAG | None = None


def get_rag() -> ExoplanetRAG:
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = ExoplanetRAG()
    return _rag_instance
