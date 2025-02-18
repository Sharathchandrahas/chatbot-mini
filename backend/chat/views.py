import os
import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from dotenv import load_dotenv
from openai import OpenAI
from langchain.document_loaders import PyPDFLoader


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        conversation = json.loads(request.POST.get("conversation", "[]"))
        user_message = ""
        if request.FILES.get("file"):  
            pdf_file = request.FILES["file"]
            file_name = f"{uuid.uuid4()}.pdf"
            saved_path = default_storage.save(f"temp/{file_name}", ContentFile(pdf_file.read()))
            file_path = default_storage.path(saved_path)
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            pdf_text = "\n".join([page.page_content for page in pages])
            default_storage.delete(saved_path)
            user_message = f"Extracted text from PDF:\n{pdf_text[:1000]}"
            conversation.append({"role": "user", "content": user_message})
            

        if request.POST.get("message"):  
            user_message = request.POST.get("message")
            conversation.append({"role": "user", "content": user_message})

        

        try:
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
            bot_response = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": bot_response})

            return JsonResponse({"response": bot_response, "conversation": conversation})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)
