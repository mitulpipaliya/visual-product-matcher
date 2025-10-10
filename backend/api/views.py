from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET'])
def health(request):
    return JsonResponse({"status": "ok"})

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):

    if 'image' not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)

    image_file = request.FILES['image']

    return JsonResponse({
        "message": "Image received!",
        "filename": image_file.name
    })