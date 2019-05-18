from django.shortcuts import render
from django.http import JsonResponse
import json
import os


# Load from file for mobile app
def guerrilla_view(request):
    file_dir = '/Users/rohil/projects/personal/pdb_processor/output/{}'

    file_name = 'guerrilla_data.json'
    with open(os.path.abspath(file_dir.format(file_name)), 'r') as f:
        data = json.load(f)

    return JsonResponse(data, safe=False)
