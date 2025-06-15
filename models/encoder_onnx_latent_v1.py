import onnxruntime as ort
import numpy as np
from PIL import Image

def preprocess_image(image: Image.Image, image_size=(128, 128)):
    image = image = image.resize(image_size).convert("RGB")
    image_np = np.array(image).astype(np.float32) / 255.0
    image_np = (image_np - 0.5) / 0.5
    image_np = np.transpose(image_np, (2, 0, 1))
    image_np = np.expand_dims(image_np, axis=0)
    return image_np

def encode_image(image: Image.Image, model_path="encoder_v1.onnx"):
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    image_tensor = preprocess_image(image)
    output = session.run(None, {input_name: image_tensor})
    return output[0]
