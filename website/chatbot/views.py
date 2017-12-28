from django.http import JsonResponse
from django.shortcuts import render
from .collections import chatbot

# Create your views here.
from django.views import View


class ChatboxView(View):
    def get(self, request):
        return render(request, 'chatbot.html', {})

def GetBotResponse(request):
    response = chatbot.get_type_input(request.GET['message'], request.GET['questioncase'])



    return JsonResponse({'response': response[0], 'case' : response[1]})