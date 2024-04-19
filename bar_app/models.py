from django.db import models

class Reference(models.Model):
    """
    Model representing a reference of beer.
    """
    id = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=100, unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Reference"
        verbose_name_plural = "References"

class Bar(models.Model):
    """
    Model representing a bar.
    """
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Bar"
        verbose_name_plural = "Bars"

class Stock(models.Model):
    """
    Model representing the stock of beer at a bar.
    """
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.reference.name} at {self.bar.name} - Stock: {self.stock}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

class OrderItem(models.Model):
    """
    Model representing an item in an order.
    """
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.reference.name} - Count: {self.count}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

class Order(models.Model):
    """
    Model representing an order.
    """
    id = models.AutoField(primary_key=True)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
