import json
import time
from pathlib import Path
from typing import Dict, List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VibeSearchEngine:
    """
    Hybrid Semantic Search & Item-to-Item Recommender using
    Sentence-Transformers (all-MiniLM-L6-v2) and FAISS IndexFlatIP.
    """

    def __init__(
        self,
        data_path: str = "data/media_catalog.json",
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.data_path = Path(data_path)
        self.model = SentenceTransformer(model_name)
        self.catalog: List[Dict] = self._load_catalog()
        self.embeddings: np.ndarray = np.array([], dtype="float32")
        self.index: faiss.IndexFlatIP = None
        self._build_index()

    def _load_catalog(self) -> List[Dict]:
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _serialize_item(self, item: Dict) -> str:
        genres = ", ".join(item["genres"])
        moods = ", ".join(item["moods"])
        return (
            f"{item['title']} ({item['type']}, {item['year']}). "
            f"Genres: {genres}. Vibes: {moods}. Plot: {item['synopsis']}"
        )

    def _build_index(self) -> None:
        documents = [self._serialize_item(item) for item in self.catalog]
        vecs = self.model.encode(documents, normalize_embeddings=True)
        self.embeddings = np.asarray(vecs, dtype="float32")

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)

    def _tag_overlap_score(self, query: str, item: Dict) -> float:
        query_lower = query.lower()
        tags = item["genres"] + item["moods"]
        matches = sum(1 for tag in tags if tag.lower() in query_lower)
        return min(matches / 2.0, 1.0)

    def search_by_vibe(
        self,
        query: str,
        top_k: int = 5,
        media_type: str = "All",
        min_rating: float = 0.0,
        semantic_weight: float = 0.80,
    ) -> Tuple[List[Dict], float]:
        if not query.strip():
            return [], 0.0

        start_t = time.perf_counter()
        query_vec = self.model.encode([query], normalize_embeddings=True)
        query_vec = np.asarray(query_vec, dtype="float32")

        scores, indices = self.index.search(query_vec, len(self.catalog))
        results = []

        for sim_score, idx in zip(scores[0], indices[0]):
            item = self.catalog[idx]

            if media_type != "All" and item["type"] != media_type:
                continue
            if item["rating"] < min_rating:
                continue

            semantic_sim = max(float(sim_score), 0.0)
            tag_score = self._tag_overlap_score(query, item)
            rating_norm = item["rating"] / 10.0

            lexical_weight = max(0.0, 0.95 - semantic_weight)
            final_score = (
                (semantic_weight * semantic_sim)
                + (lexical_weight * tag_score)
                + (0.05 * rating_norm)
            )

            results.append(
                {
                    **item,
                    "semantic_score": round(semantic_sim * 100, 1),
                    "tag_match": round(tag_score * 100, 1),
                    "final_score": round(final_score * 100, 1),
                }
            )

        results.sort(key=lambda x: x["final_score"], reverse=True)
        latency_ms = round((time.perf_counter() - start_t) * 1000, 2)
        return results[:top_k], latency_ms

    def recommend_similar(self, title: str, top_k: int = 4) -> List[Dict]:
        target_idx = next(
            (i for i, item in enumerate(self.catalog) if item["title"] == title), None
        )
        if target_idx is None:
            return []

        target_vec = self.embeddings[target_idx : target_idx + 1]
        scores, indices = self.index.search(target_vec, top_k + 1)

        recs = []
        for sim_score, idx in zip(scores[0], indices[0]):
            if idx == target_idx:
                continue
            item = self.catalog[idx]
            recs.append(
                {
                    **item,
                    "similarity_score": round(max(float(sim_score), 0.0) * 100, 1),
                }
            )
        return recs[:top_k]

    def get_all_titles(self) -> List[str]:
        return sorted([item["title"] for item in self.catalog])
