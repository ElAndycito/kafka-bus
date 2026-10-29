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
  "appearance_id": "v01-t0001",
  "video_id": "v01",
  "track_id": 1,
  "embedding": [512 numeros, normalizado L2],
  "crop_path": "data/crops/v01-t0001.jpg",
  "t_start": 12.4,
  "t_end": 15.9
}
```

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