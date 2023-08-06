import os

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests

PROXY_URL = os.getenv("PROXY_URL", None)
proxies = None
if PROXY_URL:
    proxies = {
        "http": PROXY_URL,
        "https:": PROXY_URL,
    }



# TODO: properly configure for custom permissions
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def proxy(request):
    try:
        full_path = request.get_full_path()
        proxied_request = requests.get(full_path[11:18] + '/' + full_path[18:], proxies=proxies)
        try:
            data = proxied_request.json()
        except:
            data = proxied_request.content
        return Response(status=proxied_request.status_code, data=data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)