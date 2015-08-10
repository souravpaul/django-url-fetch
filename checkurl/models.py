from django.db import models

# Create your models here.

class CheckURL(models.Model):
	key=models.CharField(max_length=200,null=False,blank=False)
	url=models.TextField(null=False,blank=False)
	status_code=models.CharField(max_length=10,null=False,blank=False)
	comment=models.CharField(max_length=200,null=False,blank=False)
	timestamp=models.DateTimeField(auto_now_add=True,auto_now=False)
	updated=models.DateTimeField(auto_now_add=False,auto_now=True)

