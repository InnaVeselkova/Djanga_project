from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from .forms import ProductForm
from .models import Product, Category
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .services import ProductService
from django.core.cache import cache


class HomeListView(ListView):
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        cache_key = f'product_list_{category_id}' if category_id else 'product_list_all'

        queryset = cache.get(cache_key)

        if queryset is None:
            # Используем сервис для получения продуктов
            queryset = ProductService.get_products_in_category(category_id)
            cache.set(cache_key, list(queryset.values('id', 'name', 'price', 'description')), timeout=60*15)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ContactsView(TemplateView):
    template_name = 'contacts.html'


def contacts_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contacts.html')


@method_decorator(cache_page(60 * 15), name='dispatch')
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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    pk_url_kwarg = 'product_id'

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        # проверка, что пользователь — владелец или модератор
        return user == product.owner or user.groups.filter(name='Модератор продуктов').exists()

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    pk_url_kwarg = 'product_id'

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        # проверка, что пользователь — владелец или модератор
        return user == product.owner or user.groups.filter(name='Модератор продуктов').exists()

class UnpublishProductView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'
    raise_exception = True  # Выдаст 403 Forbidden при отсутствии права

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.is_published = False
        product.save()
        return redirect('catalog:product_detail', pk=product.id)

class DeleteProductView(PermissionRequiredMixin, View):
    permission_required = 'catalog.delete_product'
    raise_exception = True  # Вернёт 403 Forbidden, если нет права

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return redirect('catalog:home')
