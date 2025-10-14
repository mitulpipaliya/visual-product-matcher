import os
import numpy as np
import django
import onnxruntime as ort
from PIL import Image

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "matcher.settings")
django.setup()
from api.models import Product

MEDIA_DIR = os.path.join(os.getcwd(), "media", "products")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "mobilenetv3small_512.onnx")
ort_sess = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])

def preprocess_image(img_path):
    img = Image.open(img_path).convert("RGB").resize((224, 224))
    arr = np.array(img).astype(np.float32)
    arr = arr / 127.5 - 1.0  
    arr = np.expand_dims(arr, axis=0)
    return arr

def get_embedding(img_path):
    x = preprocess_image(img_path)
    features = ort_sess.run(None, {"input": x})[0]
    features = features.flatten()
    features = features / np.linalg.norm(features)
    return features.tolist()

products = Product.objects.all()
for product in products:
    img_path = os.path.join(MEDIA_DIR, os.path.basename(product.image.name))
    embedding = get_embedding(img_path)
    product.embedding = embedding
    product.save()
    print(f"Inserted for: {product.name}")

print("Over..")