from django.contrib import admin
from .models import Category, Author, Book, News, AuthorCategory, ContactMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(AuthorCategory)
class AuthorCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_popular', 'get_categories']
    list_filter = ['is_popular', 'categories']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    filter_horizontal = ['categories']  # Добавляем удобный выбор категорий
    
    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Категории'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_available', 'is_bestseller', 'is_new']
    list_filter = ['is_available', 'is_bestseller', 'is_new', 'categories', 'publication_date']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'author__name']
    filter_horizontal = ['categories']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'publish_date', 'views_count', 'is_published']
    list_filter = ['category', 'is_published', 'publish_date']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_processed']
    list_filter = ['is_processed', 'subject', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_processed']
    actions = ['mark_as_processed', 'mark_as_unprocessed']
    
    def mark_as_processed(self, request, queryset):
        queryset.update(is_processed=True)
    mark_as_processed.short_description = "Отметить как обработанные"
    
    def mark_as_unprocessed(self, request, queryset):
        queryset.update(is_processed=False)
    mark_as_unprocessed.short_description = "Отметить как необработанные"