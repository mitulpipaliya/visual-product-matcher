import os
import numpy as np
import django
from tensorflow.keras.applications.efficientnet_v2 import EfficientNetV2B2, preprocess_input
from tensorflow.keras.preprocessing import image as keras_image

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "matcher.settings")
django.setup()
from api.models import Product

MEDIA_DIR = os.path.join(os.getcwd(), "media", "products")

base_model = EfficientNetV2B2(
    include_top=False,
    pooling='avg',
    weights='imagenet'
)

def get_embedding(img_path):
    img = keras_image.load_img(img_path, target_size=(384, 384))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = base_model.predict(x, verbose=0)
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
