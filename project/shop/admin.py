from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price_at_purchase']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Информация покупателя', {'fields': ('user', 'full_name', 'phone', 'address')}),
        ('Статус', {'fields': ('status', 'created_at', 'updated_at')}),
    )