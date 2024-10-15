from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    heading = models.CharField(max_length=100, verbose_name='заголовок')
    slug = models.CharField(max_length=100, verbose_name='транскрипция')
    content = models.TextField(verbose_name='содержание')
    image = models.ImageField(upload_to='images/', **NULLABLE, verbose_name="картинка")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    sign_of_publication = models.CharField(max_length=200, **NULLABLE, verbose_name="причина публикации")
    views = models.IntegerField(verbose_name="количество просмотров", default=0)
    is_accepted = models.BooleanField(default=True)

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        ordering = ('heading',)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='images/', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория', **NULLABLE)
    price_per_unit = models.IntegerField(verbose_name='цена за шт')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_modification_date = models.DateTimeField(auto_now=True, verbose_name='последние изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ('name', 'category',)
