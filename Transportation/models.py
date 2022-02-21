from django.db import models


class Shipping(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12,decimal_places=2)

    def __str__(self):
        return self.title

class Address(models.Model):
    user = models.ForeignKey('User.User',on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    postalCode = models.CharField(max_length=30)
    address = models.CharField(max_length=550)

    def __str__(self):
        return self.user.__str__()

    def getTextAddress(self):
        return f"{self.city} - {self.postalCode} - {self.address}"