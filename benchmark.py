from src.engine import VibeSearchEngine

TEST_QUERIES = [
    "time travel mystery with complex family secrets",
    "lonely programmer falls in love with an AI",
    "cozy heartwarming romance in winter",
    "college friends and engineering pressure comedy",
    "mind-bending dream heist thriller",
]


def run_benchmark():
    engine = VibeSearchEngine("data/media_catalog.json")
    latencies = []

    print("=" * 60)
    print("VibeSearch Retrieval Latency & Relevance Benchmark")
    print("=" * 60)

    for q in TEST_QUERIES:
        results, latency = engine.search_by_vibe(q, top_k=3)
        latencies.append(latency)
        top_titles = [f"{r['title']} ({r['final_score']}%)" for r in results]
        print(f"\nQuery: {q}")
        print(f"Latency: {latency} ms")
        print(f"Top-3:   {', '.join(top_titles)}")

    avg_latency = round(sum(latencies) / len(latencies), 2)
    print("\n" + "=" * 60)
    print(f"Average End-to-End Query Latency: {avg_latency} ms")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()
