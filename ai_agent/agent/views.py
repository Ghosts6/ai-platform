from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser

from django.conf import settings
from .agent_manager import AgentRouter
from ai_agent.core_services.models import ChatSession, ChatMessage
from asgiref.sync import async_to_sync, sync_to_async
import os
import uuid
import logging

logger = logging.getLogger(__name__)

router = AgentRouter()

class IndexView(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to the AIAgent API. Please use the /api/agent/respond endpoint to interact with agents.'})


class AgentResponseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        return async_to_sync(self.async_post)(request, *args, **kwargs)

    async def async_post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        session_id = request.data.get('session_id')
        agent_key = request.data.get('agent')
        
        if not prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

        file_path = None
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            # Create a temporary directory if it doesn't exist
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Create a unique filename to avoid overwrites
            file_name = f"{uuid.uuid4()}_{uploaded_file.name}"
            file_path = os.path.join(temp_dir, file_name)
            
            # Write the uploaded file to the temporary location
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        
        try:
            response_data = await router.route(
                prompt,
                user=request.user,
                agent_key=agent_key,
                file_path=file_path
            )

            if request.user.is_authenticated:
                session = None
                if session_id:
                    try:
                        session = await sync_to_async(ChatSession.objects.get)(id=session_id, user=request.user)
                    except ChatSession.DoesNotExist:
                        session = await sync_to_async(ChatSession.objects.create)(user=request.user)
                else:
                    session = await sync_to_async(ChatSession.objects.create)(user=request.user)

                # Extract the string for saving, but send the full object back
                if isinstance(response_data, dict) and 'result' in response_data:
                    text_to_save = response_data['result']
                else:
                    text_to_save = response_data
                
                await sync_to_async(ChatMessage.objects.create)(session=session, sender='user', text=prompt)
                await sync_to_async(ChatMessage.objects.create)(session=session, sender='agent', text=text_to_save)
                
                return Response({'response': response_data, 'session_id': str(session.id)}, status=status.HTTP_200_OK)
            else:
                return Response({'response': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error processing agent request: {e}", exc_info=True)
            return Response({'error': 'An unexpected error occurred during agent processing.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Clean up the temporary file if it was created
            if file_path and os.path.exists(file_path):
                os.remove(file_path)