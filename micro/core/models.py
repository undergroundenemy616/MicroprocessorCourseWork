from django.db import models

class User(models.Model):
    name = models.CharField(max_length=256)
    
    def __repr__(self):
        return self.name