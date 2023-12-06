from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv
import os
import requests
from langchain.chains import LLMChain
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
import json
import asyncio
from django.http import JsonResponse
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from django.contrib.auth.decorators import login_required

load_dotenv()

HUGGINGFACE_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN')
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


@login_required
def chatbot(request):
    return render(request,'chatbot/chat.html')

# def getResponse(request):
#     user_message = request.GET.get('userMessage')
#     print(user_message)
#     output = query({
# 	"inputs": f"{user_message}",
#     })
#     print(output)
#     return HttpResponse(output)


MODEL_KWARGS = {
    "mistral": {
        "model": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        "model_file": "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    }
}

llm_chain = None

TEMPLATE = """<s>[INST] You are a friendly chat bot who's willing to help answer the user and you are also honest and when you don't know any answer you just say I don't know.:
{user_input} [/INST] </s>
"""

async def query_llm(contents: str):
    global llm_chain
    if llm_chain is None:
        config = {"max_new_tokens": 1000, "temperature": 0.5}
        llm = CTransformers(**MODEL_KWARGS["mistral"], config=config)
        prompt = PromptTemplate(template=TEMPLATE, input_variables=["user_input"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)

    response = await llm_chain.apredict(user_input=contents)
    return response


@login_required
def get_response(request):
    if request.method == 'GET':
        user_message = request.GET.get('userMessage')
        print(user_message)

        # Use asyncio.run to call the asynchronous function
        output = asyncio.run(query_llm(user_message))
        print(output)
        response_data = {"AI_response": output}

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method"})





	