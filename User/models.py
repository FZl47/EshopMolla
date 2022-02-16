from django.db import models
from django.contrib.auth import models


class User(models.AbstractUser):
    pass

    def getCart(self):
        return self.cart_set.first()

    def getWishList(self):
        return self.wishlist_set.first()




