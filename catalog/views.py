from django.forms import inlineformset_factory
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


class ProductDetailView(DetailView):
    """
    View for displaying the details of a single product.
    """
    model = Product


class ProductCreateView(CreateView):
    """
    View for creating a new product.
    """
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        """
        Redirect to the product detail page after successful creation.
        """
        return reverse_lazy('catalog:view_product', args=[self.kwargs.get('pk')])


class ProductUpdateView(UpdateView):
    """
    View for updating an existing product.
    """
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        """
        Redirect to the product detail page after a successful update.
        """
        return reverse_lazy('catalog:view_product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        """
        Add an inline formset for managing product versions to the context.
        """
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        """
        Validate both the product form and the inline formset before saving.
        """
        context_data = self.get_context_data()
        formset = context_data['formset']
        if formset.is_valid() and form.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(DeleteView):
    """
    View for deleting a product.
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')


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
    View for deleting a blog post.
    """
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')