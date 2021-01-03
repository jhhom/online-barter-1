from django.db import models
from django.conf import settings
from django.db.models.deletion import DO_NOTHING

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                            default='default.png')
    
    def __str__(self):
        return f'Profile for user {self.user.username}'

# Create your models here.
class Item(models.Model):
    NEW = 'NW'
    USED = 'US'
    ITEM_CONDITION_CHOICES = [
        (NEW, 'New'),
        (USED, 'Used')
    ]

    GROCERY = 'GR'
    STATIONERY = 'ST'
    BOOK = 'BK'
    ELECTRONICS = 'ET'
    DIGITAL_ACCESSORIES = 'DA'
    SPARE_PARTS = 'SP'
    TOYS_GAMES = 'TG'
    AUTOMOTIVE = 'AT'
    TOOLS = 'TL'
    ITEM_CATEGORIES = [
        (GROCERY, 'Grocery'),
        (STATIONERY, 'Stationery'),
        (BOOK, 'Book'),
        (ELECTRONICS, 'Electronics'),
        (DIGITAL_ACCESSORIES, 'Digital Accessories'),
        (SPARE_PARTS, 'Spare Parts'),
        (TOYS_GAMES, 'Toys & Games'),
        (AUTOMOTIVE, 'Automotives'),
        (TOOLS, 'Tools'),
    ]


    title = models.CharField(max_length=120)
    condition = models.CharField(
        max_length=2,
        choices=ITEM_CONDITION_CHOICES,
        default=NEW
    )
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    listed_date = models.DateField(auto_now_add=True)
    category = models.CharField(
        max_length=2,
        choices=ITEM_CATEGORIES,
        default=GROCERY
    )
    # Automatically create owner for this field
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_by')
    favourited_by = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='favourited_by',
        blank=True)

class Barter(models.Model):
    BARTER_STATUS = [
        ('PN', 'Pending'),
        ('RJ', 'Rejected'),
        ('SC', 'Successful')
    ]
    item = models.ForeignKey(Item,
        on_delete=models.CASCADE,
        related_name='request')
    offer = models.ForeignKey(Item,
        on_delete=models.CASCADE,
        related_name='offer')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    requested_date = models.DateField(auto_now_add=True)
    complete_date = models.DateField(null=True)
    status = models.CharField(
        max_length=2,
        choices=BARTER_STATUS,
        default='PN'
    )
    