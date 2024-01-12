from django.db import models

# Create your models here.

# While creating the foreign key, you have to ensure that the category cannot be
# deleted before all the related menu items are deleted first and this is done using
# on_delete=models.PROTECT


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    def __str__(self): # to display the title in the admin page instead of id
        return self.title
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT,default=1)#for adding field in exiting model, add default value

# before you add foreign key, you have to create the model first and add some data into it, because we set default = 1

from django.db import models
from django.contrib.auth.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem_id =  models.SmallIntegerField()
    rating = models.SmallIntegerField()
    #def __str__(self):
    #  return self.user