from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
            name = models.CharField(max_length=200,
                                    db_index=True, verbose_name="类名"),
            slug = models.SlugField(max_length=200,
                                    db_index=True,
                                    unique=True,
				   verbose_name="分类slug")
        )

    class Meta:
        # ordering = ('name',)
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('shop:product_list_by_category',
                           args=[self.slug])


class Product(TranslatableModel):
    translations = TranslatedFields(
            name = models.CharField(max_length=200, db_index=True, verbose_name="产品名"),
            slug = models.SlugField(verbose_name="产品slug", max_length=200, db_index=True),
            description = models.TextField(blank=True, verbose_name="产品描述")
        )
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE,
				verbose_name="产品分类")
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True, verbose_name="产品图片")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="产品价格")
    available = models.BooleanField(default=True, verbose_name="可购买的")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
    #    ordering = ('name',)
    #    index_together = (('id', 'slug'),)
        verbose_name = '产品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('shop:product_detail',
                           args=[self.id, self.slug])
