from django.urls import path

from catalog import views

# Namespace for the catalog app.
app_name = 'catalog'

urlpatterns = [
    # URL pattern for the contact page.
    path('contacts/', views.ContactTemplate.as_view(), name='contact'),

    # URL pattern for listing all products.
    path('products/', views.ProductListView.as_view(), name='product_list'),

    # URL pattern for viewing the details of a single product.
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='view_product'),

    # URL pattern for creating a new product.
    path('product/create/', views.ProductCreateView.as_view(), name='create_product'),

    # URL pattern for editing an existing product.
    path('product/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='edit_product'),

    # URL pattern for deleting a product.
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),

    # URL pattern for listing all blog posts.
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),

    # URL pattern for creating a new blog post.
    path('blog/create/', views.BlogCreateView.as_view(), name='create_blog'),

    # URL pattern for editing an existing blog post.
    path('blog/edit/<str:slug>/', views.BlogUpdateView.as_view(), name='edit_blog'),

    # URL pattern for deleting a blog post.
    path('blog/delete/<str:slug>/', views.BlogDeleteView.as_view(), name='delete_view'),

    # URL pattern for viewing the details of a single blog post.
    path('blog/<str:slug>/', views.BlogDetailView.as_view(), name='view_blog'),
]
