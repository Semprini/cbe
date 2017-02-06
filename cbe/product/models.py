from django.db import models

from cbe.customer.models import Customer


class ProductCategory(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProductOffering(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.TextField()

    categories = models.ManyToManyField('ProductCategory', blank=True)

    retail_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Promotion(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    categories = models.ManyToManyField('ProductCategory', blank=True)
    products = models.ManyToManyField('ProductOffering', blank=True)
    customers = models.ManyToManyField(Customer, blank=True)

    def __str__(self):
        return self.name
