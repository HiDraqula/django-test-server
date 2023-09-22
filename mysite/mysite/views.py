# In views.py of your app
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse , JsonResponse 
import json 
from pprint import pprint 

@api_view(['GET', 'POST'])
def test(request):
    # if request.method == 'POST':
    post_data_str = request.body.decode('utf-8')
    # Parse the JSON string to a Python dictionary
    post_data_dict = json.loads(post_data_str)
    data = {'postData': post_data_dict}  # No need to dump it again to JSON
    pprint(data)
    return JsonResponse(data, safe=False)  # Use safe=False to prevent escaping
    # if request.method == 'GET':
    #     # Implement your GET logic here
    #     data = {
    #         "message": "This is a GET request.",
    #     }
    #     return Response(data, status=status.HTTP_200_OK)
    
    # elif request.method == 'POST':
    #     # Implement your POST logic here
    #     received_data = request.data  # Get data from the request
    #     # Process the received data as needed
    #     data = {
    #         "message": "This is a POST request.",
    #         "received_data": received_data,
    #     }
    #     return Response(data, status=status.HTTP_201_CREATED)

        