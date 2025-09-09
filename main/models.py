import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('price', 'Price'),
        ('shoes', 'Shoes'),
        ('jersey', 'Jersey'),
        ('ball', 'Ball'),
        ('headband', 'Headband'),
        ('cone', 'Cone'),
        ('vest', 'Vest'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @property
    def is_premium(self):
        return self.category in ['shoes', 'ball'] and self.price > 1500000
    
    def is_training_gear(self):
        return self.category in ['cone', 'vest', 'headband']


