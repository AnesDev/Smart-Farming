import os
import numpy as np
import pandas as pd
from PIL import Image
from models.encoder_onnx_latent_v1 import encode_image
import random

# === CONFIG ===
IMAGE_DIR = "data/images"
CAE_MODEL_PATH = "models/encoder_v1.onnx"

# === Collect image paths ===
image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
if not image_files:
    raise RuntimeError("Aucune image trouvée dans le dossier : images")

# === Encode images and generate one row per image ===
data = []
for img_name in image_files:
    img_path = os.path.join(IMAGE_DIR, img_name)
    img = Image.open(img_path)
    vec = encode_image(img, model_path=CAE_MODEL_PATH).squeeze()

    température = round(random.uniform(15, 35), 2)
    humidité = round(random.uniform(30, 90), 2)
    humidité_sol = round(random.uniform(10, 60), 2)
    lumière = round(random.uniform(100, 1000), 2)
    pH_sol = round(random.uniform(5.0, 8.0), 2)
    CO2 = round(random.uniform(300, 900), 2)

    row = [img_name, température, humidité, humidité_sol, lumière, pH_sol, CO2, str(vec.tolist())]
    data.append(row)

# === Save to CSV ===
columns = ['nom_image', 'température', 'humidité', 'humidité_sol', 'lumière', 'pH_sol', 'CO2', 'vecteur']

df = pd.DataFrame(data, columns=columns)
df.to_csv("synthetic_data.csv", index=False)
print("CSV sauvegardé")
