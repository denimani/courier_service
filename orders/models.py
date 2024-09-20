from django.db import models

NULLABLE = {
    'null': True,
    'blank': True
}


class DeliveryRequest(models.Model):
    """
    Модель заявки
    """
    PACKAGE_TYPE_CHOICES = [
        ('Письмо', 'Письмо'),
        ('Бандероль', 'Бандероль'),
        ('Габаритный груз', 'Габаритный груз')
    ]

    CITY_CHOICES = [
        ('Казань', 'Казань'),
        ('Набережные Челны', 'Набережные Челны'),
        ('Нижнекамск', 'Нижнекамск'),
        ('Альметьевск', 'Альметьевск'),
        ('Зеленодольск', 'Зеленодольск'),
    ]

    internal_id = models.AutoField(primary_key=True, verbose_name='Внутренний айди заявки')
    city = models.CharField(max_length=255, choices=CITY_CHOICES, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    delivery_date = models.DateField(verbose_name='Дата доставки')
    delivery_time = models.TimeField(verbose_name='Время доставки')
    customer = models.CharField(max_length=255, verbose_name='Клиент')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    package_type = models.CharField(max_length=255, choices=PACKAGE_TYPE_CHOICES, verbose_name='Тип посылки')
    distance = models.FloatField(verbose_name='Расстояние до склада', **NULLABLE)
    load_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')

    def __str__(self):
        return f'Заявка {self.internal_id} - {self.customer}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class DeliveryStatusCurrent(models.Model):
    """
    Класс для хранения текущего статуса доставки
    """
    STATUS_TYPES = [
        ('New', 'New'),
        ('Done', 'Done'),
        ('Canceled', 'Canceled'),
        ('Handed to courier', 'Handed to courier'),
        ('In progress', 'In progress'),
    ]

    internal_id = models.ForeignKey(DeliveryRequest, on_delete=models.CASCADE, verbose_name='Внутренний айди заявки')
    status_name = models.CharField(max_length=255, choices=STATUS_TYPES, verbose_name='Текущий статус заявки')
    load_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления статуса заявки')

    def __str__(self):
        return f'{self.internal_id} - {self.status_name}'

    class Meta:
        verbose_name = 'Текущий статус заявки'
        verbose_name_plural = 'Текущие статусы заявок'


class DeliveryRequestStatusHistory(models.Model):
    """
    Класс для хранения истории статуса доставки
    """
    internal_id = models.ForeignKey(DeliveryRequest, on_delete=models.CASCADE, verbose_name='Внутренний айди заявки')
    status_name = models.CharField(max_length=255, verbose_name='Cтатус заявки')
    load_date = models.DateTimeField(verbose_name='Дата обновления статуса заявки')

    def __str__(self):
        return f'{self.internal_id} - {self.status_name}'

    class Meta:
        verbose_name = 'История статуса заявки'
        verbose_name_plural = 'История статусов заявок'
