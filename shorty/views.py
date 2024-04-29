from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import Context, Template

from .models import URL

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests
import json

def shortenURL(longURL):
    api_url = "https://smolurl.com/api/links"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = json.dumps({"url": longURL})
    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 201:
        result = response.json()
        entry = URL.objects.create(
            shortURL=result['data']['short_url'],
            longURL=result['data']['destination_url']
        )
        return {
            "short_url": result['data']['short_url'],
            "destination_url": result['data']['destination_url']
        }
    else:
        return "Error: " + response.text

def lengthenURL(shortURL):
    try:
        longURL = URL.objects.get(shortURL=shortURL)
        return {"short_url": shortURL, "destination_url": longURL.longURL}
    except URL.DoesNotExist:
        return "Error: URL not found"

def index(request):
    template_path = '/var/task/shorty/templates/index.html'

    with open(template_path, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    
    context = {}
    
    html = template.render(Context(context))
    
    return HttpResponse(html)

class ShortenAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        long_url = request.data.get('url')
        if not long_url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        result = shortenURL(long_url)
        print(result)
        return Response(result, status=status.HTTP_201_CREATED if 'short_url' in result else status.HTTP_400_BAD_REQUEST)

class LengthenAPIView(APIView):
    def post(self, request, *args, **kwargs):
        short_url = request.data.get('short_url')
        if not short_url:
            return Response({'error': 'Short URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        result = lengthenURL(short_url)
        return Response(result, status=status.HTTP_200_OK if 'destination_url' in result else status.HTTP_404_NOT_FOUND)
