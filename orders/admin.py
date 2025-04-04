from django.contrib import admin

from orders.models import Category, Item, Order


class OrderInline(admin.TabularInline):
    """Displaying items with orderы in the admin panel."""
    model = Order.items.through


class OrderAdmin(admin.ModelAdmin):
    """Displaying orders in the admin panel."""
    inlines = [OrderInline]
    search_fields = ('table_number', 'status')


class ItemAdmin(admin.ModelAdmin):
    """Displaying items in the admin panel."""
    list_display = ('name', 'slug', 'description', 'price')


class CategoryAdmin(admin.ModelAdmin):
    """Displaying categories in the admin panel."""
    list_display = ('name', 'slug', 'description')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
