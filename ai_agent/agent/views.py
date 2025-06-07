from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .agent_manager import AgentRouter
from core_services.models import AgentMemory

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

@csrf_exempt
def agent_memory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            agent = data.get('agent')
            key = data.get('key')
            value = data.get('value')
            if not (agent and key and value is not None):
                return JsonResponse({'error': 'Missing agent, key, or value'}, status=400)
            AgentMemory.objects.update_or_create(
                agent_name=agent, key=key, defaults={'value': value}
            )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'GET':
        agent = request.GET.get('agent')
        key = request.GET.get('key')
        if not (agent and key):
            return JsonResponse({'error': 'Missing agent or key'}, status=400)
        try:
            value = AgentMemory.objects.get(agent_name=agent, key=key).value
            return JsonResponse({'agent': agent, 'key': key, 'value': value})
        except AgentMemory.DoesNotExist:
            return JsonResponse({'agent': agent, 'key': key, 'value': None})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def agent_memory_list(request):
    if request.method == 'GET':
        agent = request.GET.get('agent')
        if not agent:
            return JsonResponse({'error': 'Missing agent'}, status=400)
        memories = AgentMemory.objects.filter(agent_name=agent)
        return JsonResponse({
            'agent': agent,
            'memories': [
                {'key': m.key, 'value': m.value, 'updated_at': m.updated_at.isoformat()} for m in memories
            ]
        })
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def agent_memory_delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            agent = data.get('agent')
            key = data.get('key')
            if not (agent and key):
                return JsonResponse({'error': 'Missing agent or key'}, status=400)
            AgentMemory.objects.filter(agent_name=agent, key=key).delete()
            return JsonResponse({'status': 'deleted'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
