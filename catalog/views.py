from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm, BlogForm
from catalog.models import Product, Blog, Version
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView


class ProductListView(ListView):
    """
    View for listing all products.
    """
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        for product in context['product_list']:
            context[product] = (product.owner == user) or user.groups.filter(name='manager').exists()
        return context


class ProductDetailView(DetailView):
    """
    View for displaying the details of a single product.
    """
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new product.
    """
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    View for updating an existing product.
    """
    model = Product
    form_class = ProductForm
    permission_required = [
        'catalog.can_change_description',
        'catalog.can_change_category',
        'catalog.can_change_is_published'
    ]

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        if user.groups.filter(name='manager').exists():
            return True
        return False

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        user = self.request.user

        if self.object.owner == user:
            return form

        if user.groups.filter(name='manager').exists():
            allowed_fields = ['description', 'category', 'is_published']
            form.fields = {key: form.fields[key] for key in allowed_fields if key in form.fields}

        return form

    def get_success_url(self):
        """
        Redirect to the product detail page after a successful update.
        """
        return reverse_lazy('catalog:view_product', args=[self.kwargs.get('pk')])

    # def get_context_data(self, **kwargs):
    #     """
    #     Add an inline formset for managing product versions to the context.
    #     """
    #     context_data = super().get_context_data(**kwargs)
    #     ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
    #     if self.request.method == 'POST':
    #         context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data['formset'] = ProductFormset(instance=self.object)
    #     return context_data


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a product.
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        user = self.request.user

        if self.object.owner == user:
            return form

    def form_valid(self, form):
        user = self.request.user
        if self.object.owner == user:
            return super().form_valid(form)


class ContactTemplate(TemplateView):
    """
    View for rendering the contact page template.
    """
    template_name = 'catalog/contact.html'


class BlogListView(ListView):
    """
    View for listing all accepted blog posts.
    """
    model = Blog

    def get_queryset(self, *args, **kwargs):
        """
        Return only blog posts that have been accepted.
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_accepted=True)
        return queryset


class BlogDetailView(DetailView):
    """
    View for displaying the details of a single blog post.

    Each time a blog post is viewed, its view count is incremented.
    """
    model = Blog

    def get_object(self, queryset=None):
        """
        Increment the view count of the blog post.
        """
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    """
    View for creating a new blog post.

    Automatically generates a slug for the blog post based on its heading.
    """
    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        """
        Redirect to the blog detail page after successful creation.
        """
        return reverse_lazy('catalog:view_blog', args=[self.object.slug])

    def form_valid(self, form):
        """
        Generate a slug from the blog heading before saving.
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.heading)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    """
    View for updating an existing blog post.

    Automatically regenerates the slug if the heading changes.
    """
    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        """
        Redirect to the blog detail page after a successful update.
        """
        return reverse_lazy('catalog:view_blog', args=[self.object.slug])

    def form_valid(self, form):
        """
        Regenerate the slug based on the updated blog heading before saving.
        """
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.heading)
            new_blog.save()

        return super().form_valid(form)


class BlogDeleteView(DeleteView):
    """
    """
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
