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
