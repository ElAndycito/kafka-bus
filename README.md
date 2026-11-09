# Bus Kafka - Proyecto integrador

Capa de mensajeria entre los modulos del sistema de reconocimiento facial.

## Flujo

Modulo 2 (tracking) -> topic `embeddings` -> Modulo 3 (clasificacion) -> topic `detecciones` -> Modulo 4 (GUI)

## Como levantarlo

Requisitos: Docker Desktop y Python 3.12.

```
docker compose up -d
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install confluent-kafka numpy
```

Crear los topics (una sola vez):

```
docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic embeddings --bootstrap-server localhost:9092
docker exec kafka /opt/kafka/bin/kafka-topics.sh --create --topic detecciones --bootstrap-server localhost:9092
```

## Como usarlo desde un modulo

```python
from bus import publish, consume

publish("embeddings", {...}, key="v01-t0001")

for msg in consume("embeddings", group_id="mi_modulo"):
    ...
```

Cada modulo debe usar un `group_id` distinto.

## Mensaje del topic `embeddings` (lo publica el modulo 2)

```json
{
  "schema_version": 1,
  "event_id": "<stream_id>:<inspector_id>:completed",
  "stream_id": "d045b3e1...",
  "cycle": 0,
  "strategy": "fixed",
  "track": {
    "track_id": 1,
    "start_time": 12.4,
    "end_time": 15.9,
    "frame_count": 25,
    "representative_embedding": [512 numeros, normalizado L2, o null],
    "mean_detection_confidence": 0.9
  },
  "clip_name": "P1E_S1_C1",
  "model": "buffalo_sc",
  "representative": {
    "crop_url": "/crops/1/0.jpg",
    "image_url": "/frames/1.jpg",
    "source_frame_index": 310,
    "bbox": [2.0, 3.0, 12.0, 13.0]
  }
}
```

Lo publica `face-rec-demo --kafka` (repo `face-rec`) con la misma estructura de sus
`tracks.jsonl`. La key es `event_id`, y el modulo 3 debe ignorar un `event_id` repetido.
En `detecciones`, `appearance_id` lleva ese mismo `event_id`.

## Mensaje del topic `detecciones` (lo publica el modulo 3)

```json
{
  "appearance_id": "v01-t0001",
  "estado": "conocido | desconocido | revision",
  "identity_id": "P-0007",
  "nombre": null,
  "score": 0.71,
  "candidatos": [["P-0007", 0.71], ["P-0003", 0.52]],
  "crop_path": "data/crops/v01-t0001.jpg"
}
```

## Pruebas con modulos falsos

En tres terminales, en este orden:
`python fake_gui.py`, `python modulo3_stub.py`, `python fake_modulo2.py`