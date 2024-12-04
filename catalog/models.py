from django.db import models

# Dictionary for fields that can be empty or null.
NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """
    A model representing a blog post.

    Attributes:
        heading (str): The title of the blog post.
        slug (str): A URL-friendly version of the title.
        content (str): The main text of the blog post.
        image (ImageField): Optional image for the blog post.
        creation_date (datetime): The date and time the blog was created.
        sign_of_publication (str): Reason for publication, optional.
        views (int): Number of views the blog has received. Default is 0.
        is_accepted (bool): Indicates if the blog post is approved. Default is True.
    """
    heading = models.CharField(max_length=100, verbose_name='заголовок')
    slug = models.CharField(max_length=100, verbose_name='транскрипция')
    content = models.TextField(verbose_name='содержание')
    image = models.ImageField(upload_to='images/', **NULLABLE, verbose_name="картинка")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    sign_of_publication = models.CharField(max_length=200, **NULLABLE, verbose_name="причина публикации")
    views = models.IntegerField(verbose_name="количество просмотров", default=0)
    is_accepted = models.BooleanField(default=True)

    def __str__(self):
        """Returns the blog post title."""
        return self.heading

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        ordering = ('heading',)


class Category(models.Model):
    """
    A model for organizing products into categories.

    Attributes:
        name (str): The name of the category.
        description (str): A description of the category.
        created_at (datetime): The date and time the category was created.
    """
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        """Returns the category name."""
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ('name',)


class Product(models.Model):
    """
    A model representing a product.

    Attributes:
        name (str): The name of the product.
        description (str): A detailed description of the product.
        image (ImageField): Optional image of the product.
        category (Category): The category the product belongs to. Can be null.
        price_per_unit (int): Price per unit of the product.
        creation_date (datetime): The date and time the product was created.
        last_modification_date (datetime): The date and time the product was last updated.
    """
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='images/', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория', **NULLABLE)
    price_per_unit = models.IntegerField(verbose_name='цена за шт')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_modification_date = models.DateTimeField(auto_now=True, verbose_name='последние изменения')

    def __str__(self):
        """Returns the product name."""
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ('name', 'category',)


class Version(models.Model):
    """
    A model representing a product version.

    Attributes:
        product (Product): The product this version is linked to.
        number (int): The version number.
        name (str): The name of the version.
        is_active (bool): Indicates if the version is active. Default is True.
    """
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.SET_NULL, verbose_name="продукт",
                                **NULLABLE)
    number = models.IntegerField(verbose_name="номер")
    name = models.CharField(max_length=150, verbose_name="название")
    is_active = models.BooleanField(default=True, verbose_name="актуальная версия")

    def __str__(self):
        """Returns the version name."""
        return self.name

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
