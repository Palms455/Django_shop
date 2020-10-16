from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код купона')
    valid_from = models.DateTimeField(verbose_name='Дата начала действия')
    valid_to = models.DateTimeField(verbose_name='Дата окончания действия')
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField(verbose_name='Активный купон')

    def __str__(self):
        return self.code



