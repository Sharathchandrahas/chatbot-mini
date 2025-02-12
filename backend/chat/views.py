import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import openai  


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        conversation = data.get("conversation", []) 
        user_message = data.get("message", "")
        conversation.append({"role": "user", "content": user_message})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
            bot_response = response['choices'][0]['message']['content']
            conversation.append({"role": "assistant", "content": bot_response})
            return JsonResponse({"response": bot_response, "conversation": conversation})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)
