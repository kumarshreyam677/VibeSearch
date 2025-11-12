import html
import streamlit as st
from src.engine import VibeSearchEngine

st.set_page_config(
    page_title="VibeSearch | Semantic Movie & Series Discovery",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom Cinema-Grade Styling ---
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1220px;
}

/* Hide default Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Hero Banner */
.hero-box {
    background: radial-gradient(circle at top right, rgba(229, 9, 20, 0.22), transparent 48%),
                linear-gradient(135deg, #131726 0%, #0D101A 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.45);
}
.hero-badge {
    display: inline-block;
    background: rgba(229, 9, 20, 0.16);
    color: #FF6B6B;
    border: 1px solid rgba(229, 9, 20, 0.35);
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-size: 2.35rem;
    font-weight: 800;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.02em;
    color: #FFFFFF;
}
.hero-sub {
    color: #9CA3AF;
    font-size: 1rem;
    margin: 0;
    max-width: 760px;
    line-height: 1.5;
}

/* Recommendation Card */
.media-card {
    background: #141824;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 1.15rem;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.32);
    height: 100%;
    display: flex;
    flex-direction: column;
}
.media-card:hover {
    transform: translateY(-4px);
    border-color: rgba(229, 9, 20, 0.5);
    box-shadow: 0 14px 32px rgba(229, 9, 20, 0.12);
}
.card-banner {
    padding: 1rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.card-type {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 3px 9px;
    border-radius: 6px;
    background: rgba(0, 0, 0, 0.45);
    color: #E5E7EB;
    backdrop-filter: blur(4px);
}
.match-pill {
    font-size: 0.82rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(16, 185, 129, 0.18);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.4);
}
.rating-pill {
    font-size: 0.82rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(245, 158, 11, 0.16);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.35);
}
.card-body {
    padding: 1.15rem 1.25rem 1.25rem 1.25rem;
    flex: 1;
    display: flex;
    flex-direction: column;
}
.card-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 0.25rem 0;
    line-height: 1.3;
}
.card-synopsis {
    font-size: 0.9rem;
    color: #D1D5DB;
    line-height: 1.52;
    margin-bottom: 0.95rem;
    flex: 1;
}
.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 0.9rem;
}
.genre-tag {
    font-size: 0.73rem;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 6px;
    background: rgba(99, 102, 241, 0.16);
    color: #A5B4FC;
    border: 1px solid rgba(99, 102, 241, 0.3);
}
.mood-tag {
    font-size: 0.73rem;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.06);
    color: #D1D5DB;
    border: 1px solid rgba(255, 255, 255, 0.09);
}
.score-footer {
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    padding-top: 0.7rem;
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #9CA3AF;
}
.score-bar-bg {
    width: 100%;
    height: 5px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 6px;
}
.score-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #E50914, #F59E0B);
}

/* Spotlight Banner for Item-to-Item */
.spotlight-card {
    background: linear-gradient(135deg, #1B1F33 0%, #121622 100%);
    border: 1px solid rgba(229, 9, 20, 0.35);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 0.75rem 0 1.4rem 0;
}

/* Section Headers */
.section-label {
    font-size: 1.15rem;
    font-weight: 700;
    color: #F9FAFB;
    margin: 1.2rem 0 0.75rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.latency-badge {
    font-size: 0.78rem;
    font-weight: 600;
    color: #34D399;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 2px 10px;
    border-radius: 999px;
}
</style>
""",
    unsafe_allow_html=True,
)


GENRE_GRADIENTS = {
    "Sci-Fi": "linear-gradient(120deg, #1E1B4B 0%, #312E81 55%, #0F172A 100%)",
    "Romance": "linear-gradient(120deg, #4C0519 0%, #881337 55%, #1E1B4B 100%)",
    "Thriller": "linear-gradient(120deg, #27272A 0%, #450A0A 60%, #09090B 100%)",
    "Mystery": "linear-gradient(120deg, #1E293B 0%, #334155 55%, #0F172A 100%)",
    "Comedy": "linear-gradient(120deg, #451A03 0%, #92400E 55%, #1C1917 100%)",
    "Anime": "linear-gradient(120deg, #3B0764 0%, #6B21A8 55%, #1E1B4B 100%)",
    "Drama": "linear-gradient(120deg, #172554 0%, #1E3A8A 55%, #0F172A 100%)",
    "Fantasy": "linear-gradient(120deg, #134E4A 0%, #115E59 55%, #0F172A 100%)",
    "Animation": "linear-gradient(120deg, #064E3B 0%, #047857 55%, #0F172A 100%)",
    "Adventure": "linear-gradient(120deg, #14532D 0%, #166534 55%, #0F172A 100%)",
}


@st.cache_resource
def load_engine() -> VibeSearchEngine:
    return VibeSearchEngine("data/media_catalog.json")


def get_banner_gradient(genres: list) -> str:
    if genres and genres[0] in GENRE_GRADIENTS:
        return GENRE_GRADIENTS[genres[0]]
    return "linear-gradient(120deg, #1F2937 0%, #111827 100%)"


def render_media_card(item: dict, mode: str = "search") -> str:
    title = html.escape(item["title"])
    synopsis = html.escape(item["synopsis"])
    m_type = html.escape(item["type"])
    year = item["year"]
    rating = item["rating"]
    grad = get_banner_gradient(item["genres"])

    genre_pills = "".join(
        f'<span class="genre-tag">{html.escape(g)}</span>' for g in item["genres"]
    )
    mood_pills = "".join(
        f'<span class="mood-tag">#{html.escape(m)}</span>' for m in item["moods"][:4]
    )

    if mode == "search":
        score = item["final_score"]
        right_badge = f'<span class="match-pill">{score}% Match</span>'
        footer_html = (
            f'<div class="score-footer">'
            f'<span>Semantic: <b>{item["semantic_score"]}%</b></span>'
            f'<span>Tag Boost: <b>{item["tag_match"]}%</b></span>'
            f'<span>⭐ <b>{rating}</b></span>'
            f'</div>'
            f'<div class="score-bar-bg"><div class="score-bar-fill" style="width: {min(score, 100)}%;"></div></div>'
        )
    elif mode == "similar":
        sim = item["similarity_score"]
        right_badge = f'<span class="match-pill">{sim}% Similar</span>'
        footer_html = (
            f'<div class="score-footer">'
            f'<span>Vector Cosine Similarity</span>'
            f'<span>⭐ <b>{rating}</b></span>'
            f'</div>'
            f'<div class="score-bar-bg"><div class="score-bar-fill" style="width: {min(sim, 100)}%;"></div></div>'
        )
    else:
        right_badge = f'<span class="rating-pill">⭐ {rating}</span>'
        footer_html = ""

    return (
        f'<div class="media-card">'
        f'<div class="card-banner" style="background: {grad};">'
        f'<span class="card-type">{m_type} • {year}</span>'
        f'{right_badge}'
        f'</div>'
        f'<div class="card-body">'
        f'<div class="card-title">{title}</div>'
        f'<div class="card-synopsis">{synopsis}</div>'
        f'<div class="tag-row">{genre_pills}{mood_pills}</div>'
        f'{footer_html}'
        f'</div>'
        f'</div>'
    )


def render_grid(items: list, mode: str = "search", cols_per_row: int = 2) -> None:
    for i in range(0, len(items), cols_per_row):
        row = items[i : i + cols_per_row]
        cols = st.columns(cols_per_row, gap="medium")
        for col, item in zip(cols, row):
            with col:
                st.markdown(render_media_card(item, mode=mode), unsafe_allow_html=True)


engine = load_engine()

# --- Hero Header ---
st.markdown(
    """
<div class="hero-box">
  <div class="hero-badge">Semantic Search • FAISS Vector Engine</div>
  <div class="hero-title">🎬 VibeSearch</div>
  <p class="hero-sub">
    Discover movies & series by <b>mood, plot, or feeling</b> instead of exact titles.
    Powered by <code>all-MiniLM-L6-v2</code> dense embeddings and hybrid re-ranking.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# --- Sidebar: Advanced Ranking Controls ---
with st.sidebar:
    st.header("⚙️ Ranking Controls")
    semantic_weight = st.slider(
        "Semantic vs. Tag Weight",
        min_value=0.20,
        max_value=0.95,
        value=0.80,
        step=0.05,
        help="Higher = relies more on dense vector meaning; Lower = boosts exact genre/mood keywords.",
    )
    top_k = st.slider("Max Recommendations", 2, 10, 6)
    st.markdown("---")
    st.markdown(
        "**How It Works**\n"
        "- **Embeddings:** 384-d vectors (`all-MiniLM-L6-v2`)\n"
        "- **Index:** `FAISS IndexFlatIP` (Cosine Similarity)\n"
        "- **Hybrid Score:** Semantic + Tag Overlap + Rating"
    )

# --- Navigation Tabs ---
tab1, tab2 = st.tabs(["🔎 Discover by Vibe", "✨ More Like This"])

with tab1:
    # Search Bar + Inline Filters
    s_col, t_col, r_col = st.columns([4, 1.2, 1.3], gap="small")
    with s_col:
        query = st.text_input(
            "What are you in the mood to watch?",
            value=st.session_state.get("vibe_query", ""),
            placeholder="e.g., mind-bending sci-fi mystery with time travel and plot twists...",
            label_visibility="collapsed",
        )
    with t_col:
        media_type = st.selectbox(
            "Type", ["All", "Movie", "Series"], label_visibility="collapsed"
        )
    with r_col:
        min_rating = st.selectbox(
            "Rating",
            [("Any Rating", 0.0), ("⭐ 7.5+", 7.5), ("⭐ 8.0+", 8.0), ("⭐ 8.5+", 8.5)],
            format_func=lambda x: x[0],
            label_visibility="collapsed",
        )[1]

    # Quick-Pick Mood Chips
    quick_vibes = [
        ("🌀 Time-Travel Mystery", "slow-burn sci-fi mystery with time travel and plot twists"),
        ("❄️ Cozy Winter Romance", "cozy heartwarming romantic drama in winter"),
        ("💻 Tech & Startup Drama", "ambitious tech startup or hacker thriller"),
        ("😂 Feel-Good Slice of Life", "wholesome feel-good comedy about college or everyday life"),
        ("🤖 Eerie AI & Psychology", "eerie psychological sci-fi about artificial intelligence"),
    ]
    chip_cols = st.columns(len(quick_vibes), gap="small")
    for idx, (label, prompt) in enumerate(quick_vibes):
        if chip_cols[idx].button(label, key=f"chip_{idx}", use_container_width=True):
            st.session_state["vibe_query"] = prompt
            st.rerun()

    if query.strip():
        results, latency_ms = engine.search_by_vibe(
            query=query,
            top_k=top_k,
            media_type=media_type,
            min_rating=min_rating,
            semantic_weight=semantic_weight,
        )
        st.markdown(
            f'<div class="section-label">Top Recommendations '
            f'<span class="latency-badge">{len(results)} matches • {latency_ms} ms</span></div>',
            unsafe_allow_html=True,
        )
        if results:
            render_grid(results, mode="search", cols_per_row=2)
        else:
            st.info("No titles matched your current filters. Try lowering the minimum rating or switching to 'All'.")
    else:
        # Homepage Showcase (so it looks like a real streaming discovery site immediately)
        st.markdown(
            '<div class="section-label">🔥 Top-Rated Picks in Catalog</div>',
            unsafe_allow_html=True,
        )
        featured = sorted(engine.catalog, key=lambda x: x["rating"], reverse=True)[:6]
        render_grid(featured, mode="browse", cols_per_row=3)

with tab2:
    selected_title = st.selectbox(
        "Choose a movie or series you loved:",
        engine.get_all_titles(),
        index=engine.get_all_titles().index("Inception")
        if "Inception" in engine.get_all_titles()
        else 0,
    )
    if selected_title:
        source_item = next(
            item for item in engine.catalog if item["title"] == selected_title
        )
        st.markdown(
            f'<div class="spotlight-card">'
            f'<div style="font-size:0.78rem;color:#FF6B6B;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">Selected Title</div>'
            f'<div style="font-size:1.55rem;font-weight:800;color:#FFF;margin:4px 0;">'
            f'{html.escape(source_item["title"])} '
            f'<span style="font-size:1rem;color:#9CA3AF;font-weight:500;">({source_item["year"]} • {source_item["type"]} • ⭐ {source_item["rating"]})</span>'
            f'</div>'
            f'<div style="color:#D1D5DB;font-size:0.95rem;line-height:1.5;">{html.escape(source_item["synopsis"])}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        recs = engine.recommend_similar(selected_title, top_k=4)
        st.markdown(
            '<div class="section-label">✨ Similar Titles via Vector Nearest-Neighbors</div>',
            unsafe_allow_html=True,
        )
        render_grid(recs, mode="similar", cols_per_row=2)
