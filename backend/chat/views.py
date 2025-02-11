from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

client = OpenAI(api_key="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")


@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_query = data.get("message", "")
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_query}])
        bot_response = response.choices[0].message.content

        return JsonResponse({"response": bot_response})
    
    return JsonResponse({"error": "Invalid request"}, status=400)
