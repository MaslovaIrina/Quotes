from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import HttpResponse
from .models import MQuote
import random
  
def adding_quote(request):
    return render(request, "add_quote.html")
 
def contacts(request):
    return render(request, "contacts.html")

def top_quotes(request):
    return render(request, 'top_quotes.html')

def do_random(request):
    return render(request, 'random.html')

def added_quote(request):
    return render(request, 'added_quote.html')


def create_result(request):
    # получаем из данных запроса POST отправленные через форму данные
    bookname = request.POST.get("bookname", "Undefined")
    lastname = request.POST.get("lastname", "Undefined")
    quote = request.POST.get("quote", "Undefined")
    weight = request.POST.get('weight')
    existing_quotes = None

    # Проверка наличия цитат в БД
    if MQuote.exists(quote, lastname):
        #если существует
        error_message = "Такая цитата уже существует"
    elif MQuote.too_much_quote(bookname, lastname):
        #если цитат из книги в БД больше 3
        error_message = "Нельзя добавить больше 3 цитат из одного произведения"
        existing_quotes = MQuote.objects.filter(
            bookname=bookname, 
            lastname=lastname)
    else: 
        #добавить цитату если проверки пройдены
        error_message = 'Цитата успешно добавлена'
        new_quote = MQuote(bookname=bookname, lastname=lastname, quote=quote, weight=weight)
        new_quote.save()

    context = {
        'error_message': error_message,
        'bookname': bookname,
        'lastname': lastname,
        'quote': quote,
        'existing_quotes': existing_quotes,
    }

    return render(request, 'added_quote.html', context)

def random_quote(request):
    """
    Функция для отображения случайной цитаты с учетом веса
    """
    quotes = MQuote.objects.all()
    
    # Если цитат нет, передаем пустой контекст
    if not quotes:
        context = {'quote': None}
        return render(request, 'random.html', context)

    # Создаем список весов для каждой цитаты
    weights = [q.weight for q in quotes]
    
    chosen_quote = random.choices(quotes, weights=weights, k=1)[0]
    chosen_quote.displays += 1
    chosen_quote.save()
    context = {
        'quote': chosen_quote,
    }
    return render(request, 'random.html', context)

@require_POST
def like_quote(request, quote_id):
    """
    Добавить лайк
    """
    quote = get_object_or_404(MQuote, pk=quote_id)
    quote.likes += 1
    quote.save()
    return redirect('random_quote')

@require_POST
def dislike_quote(request, quote_id):
    """
    Добавить дизлайк
    """
    quote = get_object_or_404(MQuote, pk=quote_id)
    quote.dislikes += 1
    quote.save()
    return redirect('random_quote')

def top_quotes(request):
    quotes = MQuote.objects.order_by('-likes')[:10]
    return render(request, 'top_quotes.html', {'quotes': quotes})


def edit_quote(request, quote_id):
    quote = get_object_or_404(MQuote, pk=quote_id)
    
    if request.method == 'POST':
        new_text = request.POST.get('quote_text')
        new_author = request.POST.get('lastname')
        new_bookname = request.POST.get('bookname')
        new_weight = request.POST.get('weight')

        # Валидация и сохранение изменений
        if new_text and new_author and new_bookname and new_weight:
            quote.quote = new_text
            quote.lastname = new_author
            quote.bookname = new_bookname
            try:
                quote.weight = int(new_weight)
            except ValueError:
                pass
            quote.save()
            return redirect('random_quote')
        else:
            error = "Пожалуйста, заполните все поля корректно."
            return render(request, 'edit_quote.html', {'quote': quote, 'error': error})
    
    return render(request, 'edit_quote.html', {'quote': quote})
