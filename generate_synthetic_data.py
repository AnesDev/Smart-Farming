import os
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime, timedelta
import random

from models.encoder_onnx_latent_v1 import encode_image

# === CONFIG ===
IMAGE_DIR = "data/images"
CAE_MODEL_PATH = "models/encoder_v1.onnx"
START_DATE = datetime(2024, 6, 1)  # Start of synthetic data

# === Collect image paths ===
image_files = sorted([f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
if not image_files:
    raise RuntimeError("Aucune image trouvée dans le dossier : images")

# === Generate synthetic data ===
data = []
for i, img_name in enumerate(image_files):
    img_path = os.path.join(IMAGE_DIR, img_name)
    img = Image.open(img_path)

    vec = encode_image(img, model_path=CAE_MODEL_PATH).squeeze()

    date = START_DATE + timedelta(days=i)
    temperature_sol = round(random.uniform(10, 35), 2)
    humidite_sol = round(random.uniform(30, 80), 2)
    temperature_air = round(random.uniform(10, 40), 2)
    humidite_air = round(random.uniform(30, 90), 2)

    row = [
        date.strftime("%Y-%m-%d"),
        temperature_sol,
        humidite_sol,
        temperature_air,
        humidite_air,
        str(vec.tolist())
    ]
    data.append(row)

# === Save to CSV ===
columns = ['date', 'temperature_sol', 'humidite_sol', 'temperature_air', 'humidite_air', 'vecteur_latent']
df = pd.DataFrame(data, columns=columns)
df.to_csv("synthetic_data_with_dates.csv", index=False)
print("✅ CSV sauvegardé avec dates")