from django.contrib import admin
from .models import CustomUser, Category, Product, Include

# Inline for Include
class IncludeInline(admin.TabularInline):
    model = Include
    extra = 1

# Product admin with IncludeInline
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [IncludeInline]
    list_display = ['name', 'price', 'stock', 'new']

# Register other models
admin.site.register(CustomUser)
admin.site.register(Category)