from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Product
from django.views.generic import ListView, DetailView, CreateView, TemplateView


class HomeListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'


class ContactsView(TemplateView):
    template_name = 'contacts.html'


def contacts_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contacts.html')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_info.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')
