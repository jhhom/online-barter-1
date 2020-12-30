from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                            blank=True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'

# Create your models here.
# TODO: add a foreign key to the person trading / uploading this item
class Item(models.Model):
    NEW = 'NW'
    USED = 'US'
    ITEM_CONDITION_CHOICES = [
        (NEW, 'New'),
        (USED, 'Used')
    ]
    title = models.CharField(max_length=120)
    condition = models.CharField(
        max_length=2,
        choices=ITEM_CONDITION_CHOICES,
        default=NEW
    )
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    # Automatically create owner for this field
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_by')
    favourited_by = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='favourited_by')

