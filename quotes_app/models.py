from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
 
class MQuote(models.Model):
    """
    Модель для хранения цитат из книг с метриками популярности.

    Attributes:
        quote (CharField): Текст цитаты (максимум 200 символов)
        lastname (CharField): Фамилия автора (максимум 30 символов)
        bookname (CharField): Название книги (максимум 50 символов)
        weight (FloatField): Вес цитаты для алгоритма выбора (0.0-100.0)
        likes (PositiveIntegerField): Количество лайков цитаты
        dislikes (PositiveIntegerField): Количество дизлайков цитаты
        displays (PositiveIntegerField): Количество показов цитаты
    """

    quote = models.CharField(max_length=200)
    lastname = models.CharField(max_length=30)
    bookname = models.CharField(max_length=50)
    weight = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],default=0.0)
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Дизлайки")
    displays = models.PositiveIntegerField(default=0)

    @classmethod
    def exists(cls, quote, lastname):
        """Проверяет, существует ли уже цитата с данным текстом и автором."""
        return cls.objects.filter(quote=quote, lastname=lastname).exists()
    
    @classmethod
    def too_much_quote(cls, bookname, lastname):
        count = cls.objects.filter(bookname=bookname, lastname=lastname).count()
        return count >= 3
