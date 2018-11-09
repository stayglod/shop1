from django.db import models
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True, verbose_name="编号")
    valid_from = models.DateTimeField(verbose_name="有效起始日期")
    valid_to = models.DateTimeField(verbose_name="有效终止日期")
    discount = models.IntegerField(verbose_name="折扣",
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)])
    active = models.BooleanField(verbose_name="有效的")

    def __str__(self):
        return self.code

    class Meta:
      verbose_name = '券'
      verbose_name_plural = verbose_name
