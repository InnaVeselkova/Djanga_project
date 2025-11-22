from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductDetailView, HomeListView, ProductCreateView, ContactsView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('home/', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:product_id>/',ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:product_id>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
