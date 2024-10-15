from django.urls import path

from catalog import views
app_name = 'catalog'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('contacts/', views.ContactTemplate.as_view(), name='contact'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='view_product'),
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/create/', views.BlogCreateView.as_view(), name='create_blog'),
    path('blog/edit/<str:slug>/', views.BlogUpdateView.as_view(), name='edit_blog'),
    path('blog/delete/<str:slug>/', views.BlogDeleteView.as_view(), name='delete_view'),
    path('blog/<str:slug>/', views.BlogDetailView.as_view(), name='view_blog'),
]