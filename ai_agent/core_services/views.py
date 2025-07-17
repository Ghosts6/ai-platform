from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ContactMessageSerializer

@api_view(['POST'])
def contact_message(request):
    if request.method == 'POST':
        print('Incoming contact POST data:', request.data)
        # Honeypot check: only save if website field is empty
        website = request.data.get('website', '')
        if website:
            print('Honeypot triggered, not saving contact.')
            return Response({'message': 'Bot detected.'}, status=status.HTTP_200_OK) # Pretend it's all good

        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            print('Serializer valid, saving contact.')
            serializer.save()
            return Response({'message': 'Your message has been sent successfully!'}, status=status.HTTP_201_CREATED)
        print('Serializer errors:', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)