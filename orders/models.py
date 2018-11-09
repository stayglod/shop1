from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    name = models.CharField(_('姓名'), max_length=50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('收货地址'), max_length=250)
    postal_code = models.CharField(_('邮政编码'), max_length=20)
    city = models.CharField(_('城市'), max_length=100)
    created = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    paid = models.BooleanField(default=False,verbose_name="支付")
    braintree_id = models.CharField(max_length=150, blank=True, verbose_name="账户ID")
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
				verbose_name="券")
    discount = models.IntegerField(default=0, verbose_name="折扣",
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)
        verbose_name = '订单'
        verbose_name_plural = verbose_name
#

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="订单",
                              related_name='items',
                              on_delete=models.CASCADE)

    product = models.ForeignKey(Product, verbose_name="产品",
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


    class Meta:
        verbose_name = '订单清单'
        verbose_name_plural = verbose_name

#
