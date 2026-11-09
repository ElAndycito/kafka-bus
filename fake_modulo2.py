from uuid import uuid4

import numpy as np
from bus import publish

stream_id = uuid4().hex
for i in range(1, 6):
    emb = np.random.randn(512)
    emb = (emb / np.linalg.norm(emb)).tolist()
    event_id = f"{stream_id}:{i}:completed"
    publish("embeddings", {
        "schema_version": 1,
        "event_id": event_id,
        "stream_id": stream_id,
        "cycle": 0,
        "strategy": "fixed",
        "track": {
            "track_id": i,
            "start_time": float(i),
            "end_time": float(i) + 2.5,
            "frame_count": 25,
            "representative_embedding": emb,
            "mean_detection_confidence": 0.9,
        },
        "clip_name": "fake",
        "model": "fake",
        "representative": {
            "crop_url": f"/crops/{i}/0.jpg",
            "image_url": f"/frames/{i}.jpg",
            "source_frame_index": i,
            "bbox": [2.0, 3.0, 12.0, 13.0],
        },
    }, key=event_id)
    print("publicado", event_id)
