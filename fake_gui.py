from bus import consume

for det in consume("detecciones", group_id="gui"):
    print("GUI recibe:", det["appearance_id"], det["estado"])