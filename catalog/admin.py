from django.contrib import admin

# Register your models here.

from .models import Farmer, Family, Vegetable, VegetableInstance

#admin.site.register(Vegetable)
#admin.site.register(Farmer)
admin.site.register(Family)
#admin.site.register(VegetableInstance)

# Define the admin class
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
admin.site.register(Farmer, FarmerAdmin)


class VegetablesInstanceInline(admin.TabularInline):
    model = VegetableInstance

# Register the Admin classes for Book using the decorator
@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ('title', 'farmer', 'display_family')
    inlines = [VegetablesInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(VegetableInstance) 
class VegetableInstanceAdmin(admin.ModelAdmin):
    list_display = ('vegetable', 'status', 'borrower', 'exp_date', 'id')
    list_filter = ('status', 'exp_date')

    fieldsets = (
        (None, {
            'fields': ('vegetable', 'harvest', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'exp_date')
        }),
    )
