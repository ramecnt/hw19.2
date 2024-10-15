from django.shortcuts import render
from django.urls import reverse_lazy
from pytils.translit import slugify

from catalog.models import Product, Blog
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ContactTemplate(TemplateView):
    template_name = 'catalog/contact.html'


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_accepted=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = ('heading', 'content', 'image', 'sign_of_publication', 'is_accepted')

    def get_success_url(self):
        return reverse_lazy('catalog:view_blog', args=[self.object.slug])

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.heading)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('heading', 'content', 'image', 'sign_of_publication', 'is_accepted')

    def get_success_url(self):
        return reverse_lazy('catalog:view_blog', args=[self.object.slug])

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.heading)
            new_blog.save()

        return super().form_valid(form)


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
