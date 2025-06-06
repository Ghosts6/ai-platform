from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .agent_manager import AgentRouter

router = AgentRouter()

def index(request):
    return JsonResponse({'message': 'Agent API root'})

@csrf_exempt
def respond_to_prompt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            if not prompt:
                return JsonResponse({'error': 'Prompt is required'}, status=400)

            response = router.route(prompt)
            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
