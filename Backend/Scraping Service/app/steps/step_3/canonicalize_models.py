"""
Auto-canonicalizer for vehicle model strings.
- Input: list of model strings (optionally with counts/frequencies)
- Output: list of clusters with a canonical model and variant members
"""
from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize
from collections import defaultdict

# --- Configuration ---
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"   # light & effective
DBSCAN_EPS = 0.18                       # cosine distance threshold (lower => stricter)
DBSCAN_MIN_SAMPLES = 1                  # min points in a cluster (1 to allow singletons)


def embed_texts(texts: List[str], model_name: str = EMBED_MODEL_NAME) -> np.ndarray:
    """Compute sentence-transformer embeddings and L2-normalize them."""
    model = SentenceTransformer(model_name)
    emb = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    emb = normalize(emb)  # unit vectors help cosine DBSCAN
    return emb

def cluster_embeddings(
    emb: np.ndarray,
    eps: float = DBSCAN_EPS,
    min_samples: int = DBSCAN_MIN_SAMPLES,
    metric: str = "cosine") -> np.ndarray:
    """
    Cluster embeddings with DBSCAN (cosine metric).
    Returns cluster labels (int array, -1 means noise).
    """
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric=metric, n_jobs=-1)
    labels = clustering.fit_predict(emb)
    return labels

def choose_canonical_for_cluster(
    models: List[str],
    indices: List[int],
    freqs: Optional[Dict[str,int]] = None) -> str:
    """
    Choose canonical model name for a cluster.
    Strategy:
      1) If freqs provided -> choose most frequent member
      2) Otherwise, pick the shortest string (after trimming) among cluster members
         or fallback to centroid-proximity.
    """
    cluster_models = [models[i] for i in indices]

    if freqs:
        # pick the highest frequency; tiebreaker: shortest name
        best = sorted(indices, key=lambda i: (-freqs.get(models[i], 0), len(models[i])))[0]
        return models[best]

    # Prefer the shortest string as canonical
    shortest_model = min(cluster_models, key=lambda s: len(s))
    return shortest_model

def build_canonical_map(
    models: List[str],
    freqs: Optional[Dict[str,int]] = None,
    model_name: str = EMBED_MODEL_NAME,
    eps: float = DBSCAN_EPS,
    min_samples: int = DBSCAN_MIN_SAMPLES,
    ) -> List[Dict]:
    """
    Main function.
    - models: list of raw model strings (may contain duplicates)
    - freqs: optional dict mapping model -> occurrence count (helps canonical selection)
    Returns list of { 'canonical': str, 'variants': [str, ...], 'count': int }
    """
    # deduplicate input list
    unique_models = list(dict.fromkeys([m.strip() for m in models if m and isinstance(m, str)]))

    if not unique_models:
        return []

    emb = embed_texts(unique_models, model_name)
    labels = cluster_embeddings(emb, eps=eps, min_samples=min_samples, metric="cosine")

    clusters = defaultdict(list)
    for idx, lbl in enumerate(labels):
        clusters[int(lbl)].append(idx)

    result = []
    for lbl, indices in clusters.items():
        # select canonical
        canonical = choose_canonical_for_cluster(unique_models, indices, freqs)
        variants = [unique_models[i] for i in indices]
        total_count = sum(freqs.get(v, 1) if freqs else 1 for v in variants)
        result.append({
            "cluster_label": lbl,
            "canonical": canonical,
            "variants": sorted(variants),
            "count": total_count
        })

    # sort by count desc
    result = sorted(result, key=lambda x: -x["count"])
    return result
