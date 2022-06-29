from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserDetails(models.Model):
    account=models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    saving=models.IntegerField(default=0)

class Portfolio(models.Model):
    userdetails=models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    stock_name=models.CharField(max_length=12)
    no_of_share=models.IntegerField(default=0)
    stock_cc=models.FloatField(default=0)  
    total_profit=models.FloatField(default=0)  
    
