from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import ProductForm
from .models import Product
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView


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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_info.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    pk_url_kwarg = 'product_id'

class ProductDeleteView(LoginRequiredMixin,DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'  # шаблон для подтверждения удаления
    success_url = reverse_lazy('catalog:home')
    pk_url_kwarg = 'product_id'
