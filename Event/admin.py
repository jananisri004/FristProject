from django.contrib import admin
from .models import Booking, DecorPlan, UserOTP, Wishlist, Rating, PlanImage


@admin.register(DecorPlan)
class DecorPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'decor_plan', 'location', 'event_date', 'status')
    list_filter = ('status', 'event_date')
    search_fields = ('user__username', 'location')


@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'rating')


@admin.register(PlanImage)
class PlanImageAdmin(admin.ModelAdmin):
    list_display = ('plan', 'image')