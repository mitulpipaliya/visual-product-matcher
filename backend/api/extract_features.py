import os
import numpy as np
import django
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing import image as keras_image

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "matcher.settings")
django.setup()
from api.models import Product

MEDIA_DIR = os.path.join(os.getcwd(), "media", "products")

base_model = MobileNetV3Small(weights="imagenet", include_top=False, pooling="avg")
embedding_layer = Dense(512, activation=None, name="embedding_layer")(base_model.output)
base_model_final = Model(inputs=base_model.input, outputs=embedding_layer)

def get_embedding(img_path):
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = base_model_final.predict(x, verbose=0)
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