from django.contrib import admin
from .models import CheckURL
# Register your models here.

class CheckURLAdmin(admin.ModelAdmin):
		class Meta:
			model=CheckURL
			

admin.site.register(CheckURL,CheckURLAdmin)
