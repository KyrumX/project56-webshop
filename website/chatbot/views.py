from django.http import JsonResponse
from django.shortcuts import render
from .collections import chatbot

# Create your views here.
from django.views import View


class ChatboxView(View):
    def get(self, request):
        return render(request, 'chatbot.html', {})

def GetBotResponse(request):
    if request.user.is_authenticated:
        print("Hello, I'm logged in")
    else:
        print("Not logged in")
    response = chatbot.get_type_input(request.GET['message'], request.GET['questioncase'], request)

    return JsonResponse({'response': response[0], 'case' : response[1]})