from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

    actions = ['mark_processing', 'mark_shipped', 'mark_delivered']

    def mark_processing(self, request, queryset):
        queryset.update(status='processing')

    def mark_shipped(self, request, queryset):
        queryset.update(status='shipped')

    def mark_delivered(self, request, queryset):
        queryset.update(status='delivered')

    mark_processing.short_description = "Mark selected orders as Processing"
    mark_shipped.short_description = "Mark selected orders as Shipped"
    mark_delivered.short_description = "Mark selected orders as Delivered"

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)