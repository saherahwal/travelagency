from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length = 50)
    country_code = models.CharField(max_length = 2)
    phone_code = models.CharField(max_length = 3, default = '000')     
    
    def __str__(self):
        return "%s" % self.country_name
