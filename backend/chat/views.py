from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API=os.getenv("OPENAI_KEY")
client = OpenAI(OPENAI_API)

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        conversation = data.get("conversation", [])  # Get conversation history
        user_message = data.get("message", "")

        conversation.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        bot_response = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": bot_response})

        return JsonResponse({"response": bot_response, "conversation": conversation})
    
    return JsonResponse({"error": "Invalid request"}, status=400)
