# decoder.py
import onnxruntime as ort
import numpy as np
from PIL import Image

def decode_vector(latent_tensor, model_path="decoder_v1.onnx"):
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    output = session.run(None, {input_name: latent_tensor})
    output_image = output[0][0]  # Assuming shape (1, C, H, W)
    output_image = np.transpose(output_image, (1, 2, 0))  # CHW → HWC
    output_image = ((output_image * 0.5) + 0.5) * 255.0
    output_image = np.clip(output_image, 0, 255).astype(np.uint8)
    return Image.fromarray(output_image)
