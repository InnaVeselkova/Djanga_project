from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def contacts(request):
    return render(request, 'contacts.html')


def contacts_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contacts.html')
