from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class AuthorCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Категория автора"
        verbose_name_plural = "Категории авторов"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя автора")
    slug = models.SlugField(unique=True, verbose_name="URL")
    bio = models.TextField(verbose_name="Биография")
    photo = models.ImageField(upload_to='authors/', blank=True, null=True, verbose_name="Фото")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    is_popular = models.BooleanField(default=False, verbose_name="Популярный автор")
    categories = models.ManyToManyField(AuthorCategory, blank=True, verbose_name="Категории")
    
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    categories = models.ManyToManyField(Category, verbose_name="Категории")
    description = models.TextField(verbose_name="Описание")
    cover_image = models.ImageField(upload_to='books/covers/', verbose_name="Обложка")
    publication_date = models.DateField(verbose_name="Дата публикации")
    is_available = models.BooleanField(default=True, verbose_name="Доступно")
    is_bestseller = models.BooleanField(default=False, verbose_name="Бестселлер")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-publication_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class News(models.Model):
    NEWS_CATEGORIES = [
        ('events', 'Мероприятия'),
        ('releases', 'Новые издания'),
        ('awards', 'Награды'),
        ('projects', 'Проекты'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL")
    content = models.TextField(verbose_name="Содержание")
    short_description = models.TextField(verbose_name="Краткое описание")
    category = models.CharField(max_length=20, choices=NEWS_CATEGORIES, verbose_name="Категория")
    image = models.ImageField(upload_to='news/', verbose_name="Изображение")
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-publish_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_related_news(self):
        return News.objects.filter(
            category=self.category,
            is_published=True
        ).exclude(id=self.id).order_by('-publish_date')[:3]