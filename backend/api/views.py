from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

import os
import numpy as np
import onnxruntime as ort
from PIL import Image
from api.models import Product

MODEL_INSTANCE = None

def load_model():
    global MODEL_INSTANCE
    if MODEL_INSTANCE is None:
        model_path = os.path.join(os.path.dirname(__file__), "models", "mobilenetv3small.onnx")
        MODEL_INSTANCE = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])

def preprocess_image(file_path):
    img = Image.open(file_path).convert("RGB").resize((224, 224))
    arr = np.array(img).astype(np.float32)
    arr = arr / 127.5 - 1.0
    arr = np.expand_dims(arr, axis=0)
    return arr

def get_embedding(img_path):
    load_model()
    x = preprocess_image(img_path)
    features = MODEL_INSTANCE.run(None, {"input": x})[0]
    features = features.flatten()
    features = features / np.linalg.norm(features)
    return features

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

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def search(request):
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)

    image_file = request.FILES['image']
    temp_dir = os.path.join('media', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, image_file.name)

    try:
        with open(temp_path, 'wb+') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        query_emb = get_embedding(temp_path)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {e}'}, status=500)
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
        except Exception:
            continue

    top_results = sorted(similarities, key=lambda x: x['similarity'], reverse=True)[:10]
    return JsonResponse({'results': top_results}, status=200)