from bus import consume, publish

for msg in consume("embeddings", group_id="clasificacion"):
    print("recibido", msg["event_id"])
    representative = msg["representative"] or {}
    publish("detecciones", {
        "appearance_id": msg["event_id"],
        "estado": "desconocido",
        "identity_id": None,
        "nombre": None,
        "score": 0.0,
        "candidatos": [],
        "crop_path": representative.get("crop_url"),
    }, key=msg["event_id"])
