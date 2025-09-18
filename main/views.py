from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, News, Category, AuthorCategory, ContactMessage
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def index(request):
    books = Book.objects.filter(is_available=True).order_by('-publication_date')[:8]
    authors = Author.objects.filter(is_popular=True)[:6]
    latest_news = News.objects.filter(is_published=True).order_by('-publish_date')[:3]
    
    context = {
        'books': books,
        'authors': authors,
        'latest_news': latest_news,
    }
    return render(request, 'main/index.html', context)

def catalog(request):
    books = Book.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    # Фильтрация по категории
    category_slug = request.GET.get('category')
    if category_slug:
        books = books.filter(categories__slug=category_slug)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(title__icontains=search_query)
    
    # Сортировка
    sort_by = request.GET.get('sort', 'new')
    if sort_by == 'popular':
        books = books.filter(is_bestseller=True)
    elif sort_by == 'title':
        books = books.order_by('title')
    
    context = {
        'books': books,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'main/catalog.html', context)

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, is_available=True)
    related_books = Book.objects.filter(
        categories__in=book.categories.all()
    ).exclude(id=book.id).distinct()[:4]
    
    context = {
        'book': book,
        'related_books': related_books,
    }
    return render(request, 'main/book_detail.html', context)

def authors(request):
    authors = Author.objects.all().order_by('name')
    
    category_slug = request.GET.get('category')
    if category_slug:
        authors = authors.filter(categories__slug=category_slug)
    
    popular_only = request.GET.get('popular')
    if popular_only:
        authors = authors.filter(is_popular=True)
    author_categories = AuthorCategory.objects.all()
    
    context = {
        'authors': authors,
        'author_categories': author_categories,
        'current_category': category_slug,
        'popular_only': popular_only,
    }
    return render(request, 'main/authors.html', context)

def author_detail(request, slug):
    author = get_object_or_404(Author, slug=slug)
    books = Book.objects.filter(author=author, is_available=True)
    
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'main/author_detail.html', context)

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def news(request):
    news_list = News.objects.filter(is_published=True).order_by('-publish_date')
    
    category = request.GET.get('category')
    if category:
        news_list = news_list.filter(category=category)
    
    context = {
        'news_list': news_list,
        'current_category': category,
    }
    return render(request, 'main/news.html', context)

def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug, is_published=True)
    news_item.views_count += 1
    news_item.save()
    
    related_news = News.objects.filter(
        category=news_item.category,
        is_published=True
    ).exclude(id=news_item.id).order_by('-publish_date')[:3]
    
    context = {
        'news_item': news_item,
        'related_news': related_news,
    }
    return render(request, 'main/news_detail.html', context)

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, is_available=True)
    related_books = Book.objects.filter(
        categories__in=book.categories.all(),
        is_available=True
    ).exclude(id=book.id).distinct()[:4]
    
    context = {
        'book': book,
        'related_books': related_books,
    }
    return render(request, 'main/book_detail.html', context)

def author_detail(request, slug):
    author = get_object_or_404(Author, slug=slug)
    books = Book.objects.filter(author=author, is_available=True)
    
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'main/author_detail.html', context)

def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug, is_published=True)
    news_item.views_count += 1
    news_item.save()
    
    related_news = News.objects.filter(
        category=news_item.category,
        is_published=True
    ).exclude(id=news_item.id).order_by('-publish_date')[:3]
    
    context = {
        'news_item': news_item,
        'related_news': related_news,
    }
    return render(request, 'main/news_detail.html', context)

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохраняем сообщение в базу данных
            contact_message = form.save()
            
            # Отправляем email уведомление
            try:
                send_mail(
                    subject=f'Новое сообщение: {contact_message.get_subject_display()}',
                    message=f'''
Имя: {contact_message.name}
Email: {contact_message.email}
Телефон: {contact_message.phone or "Не указан"}
Тема: {contact_message.get_subject_display()}
Сообщение:
{contact_message.message}
                    
Дата: {contact_message.created_at.strftime("%d.%m.%Y %H:%M")}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                # Логируем ошибку отправки email, но не прерываем выполнение
                print(f"Ошибка отправки email: {e}")
            
            # Показываем сообщение об успехе
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('contacts')
    else:
        form = ContactForm()
    
    return render(request, 'main/contacts.html', {'form': form})