from django.shortcuts import render
from django.http.response import JsonResponse

from .models import Coin


def index(request):
    return render(request, 'index.html')

def get_coins_list(request):
    coins = list(Coin.objects.values())
    return JsonResponse({'coins': coins}, status=200)
