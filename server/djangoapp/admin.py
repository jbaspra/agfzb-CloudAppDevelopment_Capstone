from django.contrib import admin
# from .models import related models
from .models import CarModel, CarMake


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'make', 'name', 'model_type', 'year']
    list_filter = ['model_type', 'make', 'id', 'year']
    search_fields = ['model_type', 'name']

# CarMakeAdmin class with CarModelInline

# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel)
