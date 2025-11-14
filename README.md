# 🎬 VibeSearch — Semantic Movie & Series Recommendation Engine

A lightweight, end-to-end **Semantic Search & Content-Based Recommender** that lets users discover movies and series by natural-language mood, theme, or plot (e.g., *"slow-burn sci-fi mystery about memory"*) rather than exact title keywords.

## Why Hybrid Semantic Search?
Standard keyword search fails when users describe a *vibe* instead of exact metadata. VibeSearch solves this by combining:
1. **Dense Vector Retrieval:** Encodes synopses, genres, and mood tags into 384-dimensional normalized embeddings using `sentence-transformers/all-MiniLM-L6-v2` and indexes them in **FAISS (`IndexFlatIP`)** for fast exact cosine similarity search.
2. **Hybrid Re-Ranking:** Blends semantic similarity with lexical genre/mood overlap and a lightweight rating tie-breaker:
   $$\text{FinalScore} = w_s \cdot \text{CosineSim} + w_l \cdot \text{TagOverlap} + 0.05 \cdot \frac{\text{Rating}}{10}$$
3. **Item-to-Item Recommendations:** Uses precomputed FAISS vectors to surface nearest-neighbor titles (*"More Like This"*).

## Project Structure
```text
vibesearch/
├── data/media_catalog.json   # Curated movie & series dataset
├── src/engine.py             # Modular embedding, FAISS indexing & hybrid ranking engine
├── app.py                    # Interactive Streamlit web app
├── benchmark.py              # Latency and Top-K retrieval sanity check
└── requirements.txt
```

## Tech Stack
- **Language:** Python 3.10+
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Vector Search:** `faiss-cpu` (`IndexFlatIP`)
- **Frontend:** Streamlit

## Quickstart
```bash
git clone https://github.com/<your-username>/vibesearch.git
cd vibesearch
pip install -r requirements.txt

# Run retrieval benchmark
python benchmark.py

# Launch web UI
streamlit run app.py
```

## Key Learnings
- L2-normalizing dense embeddings allows `FAISS IndexFlatIP` (inner product) to compute exact cosine similarity without extra overhead.
- Pure semantic search can occasionally over-index on plot phrasing; adding a tunable lexical tag-overlap weight improves ranking precision for explicit genre/mood queries.

**Live Demo:** https://vibesearch-sks.streamlit.app/
