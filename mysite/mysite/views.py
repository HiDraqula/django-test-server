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

import json
import requests
import imghdr
from django.http import JsonResponse
from qr_code.qrcode import QRCode, OMEGA_CHARSET

def extract_qr_code(request):
    if request.method == 'POST':
        try:
            # Retrieve the JSON data from the request body
            post_data = json.loads(request.body.decode('utf-8'))

            # Extract the last_message field from the JSON data
            last_message = post_data.get('last_message', '')

            # Check if last_message is a URL pointing to an image
            if last_message and is_image_url(last_message):
                # Use a QR code library to decode the QR code
                extracted_text = decode_qr_code(last_message)

                if extracted_text:
                    # Respond with the extracted text
                    return JsonResponse({'message': 'QR code extracted', 'text': extracted_text})
                else:
                    # Respond with a message indicating no QR code found
                    return JsonResponse({'message': 'No QR code found in the image'})

            # Respond with a message indicating no valid image URL
            return JsonResponse({'message': 'No valid image URL'})

        except json.JSONDecodeError:
            # Respond with an error message for invalid JSON data
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    # Respond with an error for unsupported HTTP methods
    return JsonResponse({'error': 'Unsupported method'}, status=405)

def is_image_url(url):
    # Send a request to the URL to check if it exists and is an image
    try:
        response = requests.head(url)
        return (
            response.status_code == 200
            and imghdr.what(None, h=requests.get(url).content) is not None
        )
    except requests.exceptions.RequestException:
        return False

def decode_qr_code(image_url):
    try:
        # You need to implement the logic to decode the QR code from the image URL here
        # Use a QR code library like qrtools or pyzbar for decoding
        # Example:
        qr = QRCode()
        qr.add_data(image_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        decoded_text = qr.decode()
        return decoded_text[0].data.decode('utf-8')
        # return "Decoded QR code text"
    except Exception as e:
        return None


# import json
# import requests
# from django.http import JsonResponse
# from PIL import Image
# import qrcode
# from io import BytesIO

# def extract_qr_code(request):
#     if request.method == 'POST':
#         try:
#             # Get the image URL from the POST data
#             image_url = request.POST.get('image_url')

#             # Fetch the image from the URL
#             response = requests.get(image_url)
#             response.raise_for_status()

#             # Open the image using Pillow (PIL)
#             img = Image.open(BytesIO(response.content))

#             # Detect and decode the QR code using the qrcode library
#             qr_code = qrcode.make(img)
#             qr_code_text = qr_code.get_data()

#             # Check if QR code data was extracted successfully
#             if qr_code_text:
#                 return JsonResponse({'message': 'QR code extracted successfully', 'qr_code_text': qr_code_text})
#             else:
#                 return JsonResponse({'message': 'No QR code found in the image'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST requests are supported'}, status=405)