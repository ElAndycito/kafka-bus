import numpy as np
from bus import publish

for i in range(5):
    emb = np.random.randn(512)
    emb = (emb / np.linalg.norm(emb)).tolist()
    publish("embeddings", {
        "appearance_id": f"v01-t{i:04d}",
        "video_id": "v01",
        "track_id": i,
        "embedding": emb,
        "crop_path": f"data/crops/v01-t{i:04d}.jpg",
        "t_start": float(i),
        "t_end": float(i) + 2.5,
    }, key=f"v01-t{i:04d}")
    print("publicado", i)