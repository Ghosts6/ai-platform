from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ContactMessage, ChatSession, ChatMessage
from .serializers import ContactMessageSerializer, ChatSessionSerializer, ChatMessageSerializer

class ContactMessageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        website = request.data.get('website', '')
        if website:
            return Response({'message': 'Bot detected.'}, status=status.HTTP_200_OK)
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your message has been sent successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)

class ChatSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            messages = session.messages.all().order_by('created_at')
            serializer = ChatMessageSerializer(messages, many=True)
            return Response(serializer.data)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Chat session not found.'}, status=404)

class LastChatSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        session = ChatSession.objects.filter(user=request.user).order_by('-created_at').first()
        if session:
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data)
        return Response({'error': 'No chat session found.'}, status=404)