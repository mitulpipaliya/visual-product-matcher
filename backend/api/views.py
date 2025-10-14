from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

import os
import numpy as np
from django.http import JsonResponse
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from api.models import Product

MODEL_INSTANCE = None

@api_view(['GET'])
def health(request):
    return JsonResponse({"status": "ok"})

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload(request):
    if 'image' not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)
    image_file = request.FILES['image']
    return JsonResponse({
        "message": "Image received!",
        "filename": image_file.name
    })

def load_model():
    global MODEL_INSTANCE
    if MODEL_INSTANCE is None:
        try:
            MODEL_INSTANCE = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
        except Exception as e:
            print(f"Error loading MobileNetV2 model: {e}")
            raise RuntimeError("ML model is not available.")

def get_embedding(img_path):
    load_model()
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    try:
        features = MODEL_INSTANCE.predict(x, verbose=0)
    except Exception as e:
        raise RuntimeError(f"Error during model prediction: {e}")
    features = features.flatten()
    features = features / np.linalg.norm(features)
    return features

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def search(request):
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)

    image_file = request.FILES['image']
    temp_dir = os.path.join('media', 'temp')
    
    try:
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, image_file.name)

        with open(temp_path, 'wb+') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        query_emb = get_embedding(temp_path)
        
    except RuntimeError as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': f"Server error during file handling: {e}"}, status=500)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    products = Product.objects.exclude(embedding__isnull=True)
    similarities = []
    
    for p in products:
        try:
            emb = np.array(p.embedding, dtype=float)
            sim = np.dot(query_emb, emb)
            
            similarities.append({
                'name': p.name,
                'category': p.category,
                'image_url': p.image.url,
                'similarity': round(float(sim), 4)
            })
        except Exception as e:
            print(f"Skipping product {p.name} due to bad embedding: {e}")
            continue

    top_results = sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:10]
    return JsonResponse({'results': top_results}, status=200)