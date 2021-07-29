from django.db import models
from accounts.models import UserModel
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'id': self.id})


class ProductVariant(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    unit_choices = [
        ('L', 'Liter(s)'),
        ('ML', 'Milliliter(s)'),
        ('KG', 'Kilogram(s)'),
        ('G', 'Gram(s)'),
        ('P', 'Piece(s)'),
    ]
    price = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(
        verbose_name='unit',
        max_length=20,
        choices=unit_choices,
        null=True,
    )

    def __str__(self):
        return (
            f'{self.product.name} , {self.size} {self.unit} , €{self.price}'
        )
