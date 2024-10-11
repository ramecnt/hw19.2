from django.urls import path

from catalog import views

urlpatterns = {
    path('', views.home, name='home'),
    path('contacts/', views.contact, name='contact'),
    path('product/<int:product_id>', views.product, name='product'),
}