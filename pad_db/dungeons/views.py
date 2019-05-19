from django.http import JsonResponse
import json
import os
from django.conf import settings


# Load from file for mobile app
def dungeons_view(request):
    file_name = 'dungeons.json'
    with open(os.path.abspath(settings.PROCESSED_FILE_DIR.format(file_name)), 'r') as f:
        data = json.load(f)

    return JsonResponse(data, safe=False)
