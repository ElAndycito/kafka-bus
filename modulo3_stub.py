from bus import consume, publish

for msg in consume("embeddings", group_id="clasificacion"):
    print("recibido", msg["appearance_id"])
    publish("detecciones", {
        "appearance_id": msg["appearance_id"],
        "estado": "desconocido",
        "identity_id": None,
        "nombre": None,
        "score": 0.0,
        "candidatos": [],
        "crop_path": msg["crop_path"],
    }, key=msg["appearance_id"])